import base64
import tempfile
import threading
import unittest
import json
import urllib.request
from pathlib import Path
from http.server import ThreadingHTTPServer
from unittest.mock import patch

from scripts import story_api_server as api


class IllustrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.cache = Path(self.temp.name)
        self.context = api.sample_story_context()

    def tearDown(self):
        self.temp.cleanup()

    def test_mock_generation_then_cache_hit(self):
        first = api.generate_illustration(
            self.context, "unused", api.DEFAULT_IMAGE_MODEL, "low",
            api.DEFAULT_GATEWAY, self.cache, mock=True,
        )
        second = api.generate_illustration(
            self.context, "unused", api.DEFAULT_IMAGE_MODEL, "low",
            api.DEFAULT_GATEWAY, self.cache, mock=True,
        )
        self.assertFalse(first["cached"])
        self.assertTrue(second["cached"])
        self.assertEqual(first["nominal_credits"], 8)
        self.assertEqual(first["credits"], 0)
        self.assertEqual(second["credits"], 0)
        self.assertEqual(first["image_path"], second["image_path"])
        self.assertGreater(Path(first["image_path"]).stat().st_size, 60)

    def test_failed_request_is_not_cached(self):
        def fail(*args):
            raise RuntimeError("simulated provider failure")

        with self.assertRaisesRegex(RuntimeError, "simulated provider failure"):
            api.generate_illustration(
                self.context, "unused", api.DEFAULT_IMAGE_MODEL, "low",
                api.DEFAULT_GATEWAY, self.cache, requester=fail,
            )
        self.assertEqual(list(self.cache.glob("*.png")), [])
        self.assertEqual(list(self.cache.glob("*.tmp")), [])

    def test_duplicate_inflight_request_is_rejected(self):
        entered = threading.Event()
        release = threading.Event()
        errors = []

        def delayed(*args):
            entered.set()
            release.wait(5)
            return {"data": [{"b64_json": base64.b64encode(api.MOCK_PNG).decode("ascii")}]} 

        def first_request():
            try:
                api.generate_illustration(
                    self.context, "unused", api.DEFAULT_IMAGE_MODEL, "low",
                    api.DEFAULT_GATEWAY, self.cache, requester=delayed,
                )
            except Exception as exc:
                errors.append(exc)

        worker = threading.Thread(target=first_request)
        worker.start()
        self.assertTrue(entered.wait(2))
        with self.assertRaisesRegex(RuntimeError, "already running"):
            api.generate_illustration(
                self.context, "unused", api.DEFAULT_IMAGE_MODEL, "low",
                api.DEFAULT_GATEWAY, self.cache, mock=True,
            )
        release.set()
        worker.join(5)
        self.assertFalse(worker.is_alive())
        self.assertEqual(errors, [])

    def test_mock_illustration_http_endpoint(self):
        api.StoryHandler.key = "unused"
        api.StoryHandler.image_model = api.DEFAULT_IMAGE_MODEL
        api.StoryHandler.image_quality = "low"
        api.StoryHandler.gateway = api.DEFAULT_GATEWAY
        api.StoryHandler.cache_dir = self.cache
        api.StoryHandler.mock_images = True
        server = ThreadingHTTPServer(("127.0.0.1", 0), api.StoryHandler)
        worker = threading.Thread(target=server.serve_forever)
        worker.start()
        try:
            request = urllib.request.Request(
                f"http://127.0.0.1:{server.server_port}/illustration",
                data=json.dumps(self.context, ensure_ascii=False).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=5) as response:
                result = json.loads(response.read().decode("utf-8"))
            self.assertTrue(result["ok"])
            self.assertTrue(result["mock"])
            self.assertEqual(result["nominal_credits"], 8)
            self.assertEqual(result["credits"], 0)
            self.assertTrue(Path(result["image_path"]).is_file())
        finally:
            server.shutdown()
            server.server_close()
            worker.join(5)

    def test_health_endpoint_reports_image_budget_without_generation(self):
        api.StoryHandler.key = "unused"
        api.StoryHandler.model = api.DEFAULT_MODEL
        api.StoryHandler.image_model = api.DEFAULT_IMAGE_MODEL
        api.StoryHandler.image_quality = "low"
        api.StoryHandler.gateway = api.DEFAULT_GATEWAY
        api.StoryHandler.cache_dir = self.cache
        api.StoryHandler.mock_images = True
        server = ThreadingHTTPServer(("127.0.0.1", 0), api.StoryHandler)
        worker = threading.Thread(target=server.serve_forever)
        worker.start()
        try:
            with urllib.request.urlopen(
                f"http://127.0.0.1:{server.server_port}/health", timeout=5
            ) as response:
                result = json.loads(response.read().decode("utf-8"))
            self.assertTrue(result["ok"])
            self.assertEqual(result["image_model"], api.DEFAULT_IMAGE_MODEL)
            self.assertEqual(result["image_credits"], 8)
            self.assertEqual(list(self.cache.glob("*.png")), [])
        finally:
            server.shutdown()
            server.server_close()
            worker.join(5)

    def test_choice_generation_uses_one_contextual_two_paragraph_request(self):
        context = {
            "opening_sentence": "The door remembered her name.",
            "last_scene": "Mina found the broken seal.",
            "story_facts": ["The seal belongs to Mina's family."],
            "previous_choices": [{"headline": "Break the seal"}],
        }
        choices = []
        for index in range(3):
            choices.append({
                "headline": f"Choice {index + 1}",
                "detail": "Take an action with a clear risk.",
                "narrative": "The action continues the prior scene. A concrete event changes the situation.\n\nThe consequence establishes a new fact. A hook leads into the next act.",
                "impact": "The consequence remains active.",
                "facts": [f"Canonical fact {index + 1}"],
            })
        response = {"output_text": json.dumps({"choices": choices})}

        with patch.object(api, "gateway_request", return_value=response) as request:
            result = api.generate_choices(context, "unused", api.DEFAULT_MODEL, api.DEFAULT_GATEWAY)

        self.assertEqual(len(result["choices"]), 3)
        request.assert_called_once()
        request_payload = request.call_args.args[1]
        prompt = request_payload["input"][0]["content"]
        self.assertEqual(request_payload["max_output_tokens"], 3200)
        self.assertIn("story_facts", prompt)
        self.assertIn("last_scene", prompt)
        self.assertIn("exactly two paragraphs", prompt)


if __name__ == "__main__":
    unittest.main()
