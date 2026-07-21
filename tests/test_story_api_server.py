import base64
import tempfile
import threading
import unittest
import json
import os
import urllib.request
from pathlib import Path
from http.server import ThreadingHTTPServer
from unittest.mock import patch

from scripts import story_api_server as api


class ProviderTests(unittest.TestCase):
    def test_provider_keys_are_never_mixed(self):
        with patch.dict(os.environ, {
            "SOGANG_API_KEY": "sogang-test-key",
            "OPENAI_API_KEY": "openai-test-key",
        }, clear=True):
            self.assertEqual(api.load_key("sogang"), "sogang-test-key")
            self.assertEqual(api.load_key("openai"), "openai-test-key")

    def test_official_openai_routes_and_image_payload(self):
        self.assertEqual(
            api.provider_url("openai", "responses"),
            "https://api.openai.com/v1/responses",
        )
        captured = {}

        def requester(url, body, key, timeout):
            captured.update(url=url, body=body, key=key)
            return {"data": [{"b64_json": base64.b64encode(api.MOCK_PNG).decode("ascii")}]}

        with tempfile.TemporaryDirectory() as temp:
            api.generate_illustration(
                api.sample_story_context(), "openai-test-key", api.DEFAULT_IMAGE_MODEL,
                "low", api.PROVIDERS["openai"]["gateway"], Path(temp),
                requester=requester, provider="openai",
            )
        self.assertEqual(captured["url"], "https://api.openai.com/v1/images/generations")
        self.assertEqual(captured["body"]["n"], 1)
        self.assertNotIn("number_of_images", captured["body"])

    def test_sogang_routes_keep_gateway_contract(self):
        self.assertEqual(
            api.provider_url("sogang", "responses"),
            "https://factchat-cloud.mindlogic.ai/v1/gateway/responses/",
        )
        self.assertEqual(
            api.provider_url("sogang", "images"),
            "https://factchat-cloud.mindlogic.ai/v1/gateway/images/generate/",
        )


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
            self.assertEqual(result["choice_schema_version"], 3)
            self.assertEqual(result["server_build"], api.SERVER_BUILD_ID)
            self.assertEqual(result["image_model"], api.DEFAULT_IMAGE_MODEL)
            self.assertEqual(result["image_credits"], 8)
            self.assertEqual(list(self.cache.glob("*.png")), [])
        finally:
            server.shutdown()
            server.server_close()
            worker.join(5)

    def test_http_choices_then_advance_contract_without_live_api(self):
        choices = [
            {"headline": f"Choice {index + 1}", "detail": "A concrete action with a risk."}
            for index in range(3)
        ]
        provider_results = [
            {"output_text": json.dumps({"choices": choices})},
            {"output_text": json.dumps({
                "scene": {
                    "paragraphs": [
                        "Mina follows the chosen clue into the flooded archive.",
                        "The recovered ledger proves the witness lied and exposes a new suspect.",
                    ],
                    "impact": "The false testimony is now established.",
                    "facts": ["The witness falsified the testimony."],
                },
                "next_choices": choices,
                "epilogue": "",
            })},
        ]
        api.StoryHandler.key = "unused"
        api.StoryHandler.model = api.DEFAULT_MODEL
        api.StoryHandler.gateway = api.DEFAULT_GATEWAY
        api.StoryHandler.cache_dir = self.cache
        server = ThreadingHTTPServer(("127.0.0.1", 0), api.StoryHandler)
        worker = threading.Thread(target=server.serve_forever)
        worker.start()
        try:
            with patch.object(api, "gateway_request", side_effect=provider_results) as gateway:
                base = f"http://127.0.0.1:{server.server_port}"
                def post(path, payload):
                    request = urllib.request.Request(
                        base + path,
                        data=json.dumps(payload).encode("utf-8"),
                        headers={"Content-Type": "application/json"},
                        method="POST",
                    )
                    with urllib.request.urlopen(request, timeout=5) as response:
                        return json.loads(response.read().decode("utf-8"))

                initial = post("/choices", {"opening_sentence": "The lake knew her name."})
                advance = post("/advance", {
                    "selected_choice": initial["choices"][1],
                    "is_final": False,
                })
                cached_advance = post("/advance", {
                    "selected_choice": initial["choices"][1],
                    "is_final": False,
                })

            self.assertEqual(gateway.call_count, 2)
            self.assertEqual(initial["kind"], "choices")
            self.assertEqual(advance["kind"], "advance")
            self.assertEqual(advance["server_build"], api.SERVER_BUILD_ID)
            self.assertEqual(len(advance["scene"]["paragraphs"]), 2)
            self.assertEqual(len(advance["next_choices"]), 3)
            self.assertFalse(advance["cached"])
            self.assertTrue(cached_advance["cached"])
            self.assertEqual(cached_advance["request_id"], advance["request_id"])
        finally:
            server.shutdown()
            server.server_close()
            worker.join(5)

    def test_initial_choice_generation_is_one_compact_request(self):
        context = {
            "opening_sentence": "The door remembered her name.",
            "genre": "mystery",
        }
        choices = []
        for index in range(3):
            choices.append({
                "headline": f"Choice {index + 1}",
                "detail": "Take an action with a clear risk.",
            })
        response = {"output_text": json.dumps({"choices": choices})}

        with patch.object(api, "gateway_request", return_value=response) as request:
            result = api.generate_choices(context, "unused", api.DEFAULT_MODEL, api.DEFAULT_GATEWAY)

        self.assertEqual(len(result["choices"]), 3)
        request.assert_called_once()
        request_payload = request.call_args.args[1]
        prompt = request_payload["input"][0]["content"]
        self.assertEqual(request_payload["max_output_tokens"], 1000)
        self.assertIn("opening_sentence", prompt)
        self.assertIn("do not write their", prompt)
        self.assertNotIn("narrative", result["choices"][0])

    def test_advance_generates_selected_scene_and_next_choices_in_one_request(self):
        next_choices = []
        for index in range(3):
            next_choices.append({
                "headline": f"Next choice {index + 1}",
                "detail": "Continue from the newly established consequence.",
            })
        response = {"output_text": json.dumps({
            "scene": {
                "paragraphs": ["The selected action unfolds in concrete detail.", "Its consequence creates the next conflict."],
                "impact": "The consequence remains active.",
                "facts": ["A canonical fact is established."],
            },
            "next_choices": next_choices,
            "epilogue": "",
        })}
        context = {
            "selected_choice": {"headline": "Open the door", "detail": "Risk being discovered."},
            "last_scene": "The door remembered her name.",
            "story_facts": [],
            "is_final": False,
        }

        with patch.object(api, "gateway_request", return_value=response) as request:
            result = api.advance_story(context, "unused", api.DEFAULT_MODEL, api.DEFAULT_GATEWAY)

        request.assert_called_once()
        request_payload = request.call_args.args[1]
        self.assertEqual(request_payload["max_output_tokens"], 2200)
        self.assertEqual(len(result["scene"]["paragraphs"]), 2)
        self.assertEqual(len(result["next_choices"]), 3)
        self.assertEqual(result["scene"]["facts"], ["A canonical fact is established."])

    def test_final_advance_returns_epilogue_without_next_choices(self):
        response = {"output_text": json.dumps({
            "scene": {"paragraphs": ["The final action begins.", "The conflict resolves."], "impact": "The journey is complete.", "facts": ["The conflict is resolved."]},
            "next_choices": [{"headline": "Ignored", "detail": "Final acts have no next choice."}],
            "epilogue": "Mina carries the truth into a changed world.",
        })}
        with patch.object(api, "gateway_request", return_value=response):
            result = api.advance_story({"is_final": True}, "unused", api.DEFAULT_MODEL, api.DEFAULT_GATEWAY)
        self.assertEqual(result["next_choices"], [])
        self.assertIn("changed world", result["epilogue"])

    def test_complete_live_cycle_uses_exactly_six_gateway_requests(self):
        compact_choices = [
            {"headline": f"Choice {index + 1}", "detail": "A concise contextual risk."}
            for index in range(3)
        ]
        initial_response = {"output_text": json.dumps({"choices": compact_choices})}
        advance_responses = []
        for act_index in range(5):
            is_final = act_index == 4
            advance_responses.append({"output_text": json.dumps({
                "scene": {
                    "paragraphs": [f"Act {act_index + 1} action unfolds.", f"Act {act_index + 1} consequence continues."],
                    "impact": f"Impact {act_index + 1}",
                    "facts": [f"Fact {act_index + 1}"],
                },
                "next_choices": [] if is_final else compact_choices,
                "epilogue": "The complete journey resolves." if is_final else "",
            })})

        with patch.object(api, "gateway_request", side_effect=[initial_response] + advance_responses) as request:
            api.generate_choices({"opening_sentence": "Begin."}, "unused", api.DEFAULT_MODEL, api.DEFAULT_GATEWAY)
            for act_index in range(5):
                api.advance_story({"is_final": act_index == 4}, "unused", api.DEFAULT_MODEL, api.DEFAULT_GATEWAY)

        self.assertEqual(request.call_count, 6)


if __name__ == "__main__":
    unittest.main()
