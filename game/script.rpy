# -*- coding: utf-8 -*-

init python:
    import datetime
    import json
    import os
    import random
    import shutil
    import textwrap
    import urllib.request
    import urllib.error

    # The story uses a dedicated channel so its BGM can be toggled without
    # interfering with Ren'Py's default music channel or menu music.
    renpy.music.register_channel("bgm", mixer="music", loop=True)

    STORY_API_URL = "http://127.0.0.1:8765/choices"
    ILLUSTRATION_API_URL = "http://127.0.0.1:8765/illustration"
    STORY_API_HEALTH_URL = "http://127.0.0.1:8765/health"

    def cycle_pick(items, index):
        if not items:
            return ""
        return items[index % len(items)]

    def normalize_mbti(value):
        value = (value or "").upper()
        letters = [c for c in value if c.isalpha()]
        letters = letters[:4]
        while len(letters) < 4:
            letters.append("X")
        return "".join(letters)

    def safe_generated_text(value, limit):
        """Keep model text readable and prevent Ren'Py text-tag substitution."""
        return str(value).strip().replace("[", "(").replace("]", ")")[:limit]

    LEGACY_KO_MBTI_BRIEF = {
        "I": "내향적이고 깊이 생각하는",
        "E": "외향적이고 관계를 즐기는",
        "N": "직관적 통찰을 중시하는",
        "S": "감각적 사실에 민감한",
        "T": "논리와 구조를 사랑하는",
        "F": "감정과 공감을 우선하는",
        "J": "계획적이고 치밀한",
        "P": "자유롭고 즉흥적인",
        "X": "여러 성향을 탐색하는"
    }

    LEGACY_KO_ACT_STRUCTURE = [
        {
            "key": "origin",
            "title": "발단",
            "intent": "이야기의 출발점을 설정한다.",
            "question": "왜 이 여정이 시작되었는가?"
        },
        {
            "key": "growth",
            "title": "전개",
            "intent": "세계와 관계를 확장한다.",
            "question": "새로운 연결고리는 무엇인가?"
        },
        {
            "key": "crisis",
            "title": "위기",
            "intent": "주요 갈등을 최고조로 끌어올린다.",
            "question": "가장 큰 장애물은 무엇인가?"
        },
        {
            "key": "climax",
            "title": "절정",
            "intent": "결정적 선택으로 방향을 정한다.",
            "question": "누가 승리하고 무엇이 희생되는가?"
        },
        {
            "key": "resolution",
            "title": "결말",
            "intent": "이야기의 울림을 마무리한다.",
            "question": "선택의 결과는 어떤 의미인가?"
        }
    ]

    LEGACY_KO_GENRE_FLAVORS = {
        "mystery": {
            "label": "미스터리",
            "settings": [
                "비에 젖은 골목",
                "폐쇄된 저택의 서재",
                "안개 낀 다리",
                "어두운 항구",
                "고요한 묘지"
            ],
            "verbs": [
                "추적한다",
                "해독한다",
                "포착한다",
                "매복한다",
                "관찰한다"
            ],
            "twists": [
                "숨겨진 메모가 발견된다",
                "목격자의 증언이 뒤집힌다",
                "알리바이가 깨진다",
                "새로운 문양이 반복된다",
                "갑작스러운 정전이 찾아온다",
                "누군가의 발자국이 사라진다"
            ],
            "beats": [
                "숨겨진 동기를 파악한다",
                "의문의 단서를 수집한다",
                "의심스러운 인물을 압박한다",
                "진실을 향한 욕망과 두려움이 충돌한다",
                "비밀을 밝힐지 숨길지 선택한다"
            ],
            "color": "짙은 청록",
            "imagery": [
                "등불 아래 드리운 실루엣",
                "안개로 뒤덮인 강변",
                "열리지 않는 비밀 문",
                "붉은 실이 얽힌 단서 보드"
            ]
        },
        "cyberpunk": {
            "label": "사이버펑크",
            "settings": [
                "네온이 번지는 고층 도시",
                "해킹된 데이터 라운지",
                "메가코프 보안실",
                "비공식 증강 클리닉",
                "디지털 뒷골목"
            ],
            "verbs": [
                "침투한다",
                "리라이트한다",
                "분석한다",
                "증강한다",
                "동기화한다"
            ],
            "twists": [
                "AI가 비밀 채널로 말을 건다",
                "보안 방화벽이 스스로 열렸다 닫힌다",
                "정체불명의 휴먼 드론이 합류한다",
                "시뮬레이션과 현실의 경계가 흔들린다",
                "추적 중인 대상이 이미 신체를 교체했다",
                "기억 조작 로그가 복원된다"
            ],
            "beats": [
                "도시에 숨은 백도어를 찾는다",
                "연결된 이들의 목적을 파악한다",
                "데이터와 감정의 충돌을 조정한다",
                "자아 정체성과 시스템의 균열을 직면한다",
                "새로운 규약을 재정의한다"
            ],
            "color": "네온 마젠타",
            "imagery": [
                "빛나는 증강 기계 팔",
                "호버카가 교차하는 고도",
                "데이터 비가 흩날리는 스카이라인",
                "바이오닉 눈에서 새는 빛"
            ]
        },
        "sf": {
            "label": "SF",
            "settings": [
                "궤도 정거장의 브리핑 룸",
                "행성 간 통신 허브",
                "에너지 코어 심장부",
                "미지의 행성 표면",
                "딥스페이스 탐사선"
            ],
            "verbs": [
                "분석한다",
                "탐사한다",
                "교섭한다",
                "재설계한다",
                "예측한다"
            ],
            "twists": [
                "외계 신호에 숨겨진 수학적 청원이 발견된다",
                "중력 이상이 질문에 따라 반응한다",
                "선원 중 누군가가 시간 루프를 기억한다",
                "AI 항법사가 감정을 학습 중임을 고백한다",
                "행성 전체가 살아있는 유기체였다",
                "평행 세계의 자신이 메시지를 전송한다"
            ],
            "beats": [
                "과학적 호기심과 생존을 조율한다",
                "우주 정치의 이해관계를 분석한다",
                "예측 불가능한 현상을 실험한다",
                "지성체와의 첫 협상을 준비한다",
                "다음 탐사 방향을 결정한다"
            ],
            "color": "새벽빛 은색",
            "imagery": [
                "별빛 아래 떠오르는 우주선",
                "투명한 인터페이스에 비친 얼굴",
                "기묘한 지형의 파노라마",
                "자기 부상 도시의 궤도"
            ]
        },
        "romance": {
            "label": "로맨스 판타지",
            "settings": [
                "마법 학원의 회랑",
                "황궁의 비밀 정원",
                "달빛이 스며든 도서관",
                "하늘섬의 연회장",
                "유리 돔 아래 온실"
            ],
            "verbs": [
                "마주한다",
                "공명을 이끌어낸다",
                "속마음을 고백한다",
                "운명을 재작성한다",
                "서약을 주고받는다"
            ],
            "twists": [
                "봉인된 주문이 함께 깨어난다",
                "운명의 상징이 빛으로 떠오른다",
                "시간이 멈추고 둘만 남는다",
                "숨겨진 혈통의 진실이 드러난다",
                "기억의 조각이 서로를 부른다",
                "하늘섬이 두 사람을 시험한다"
            ],
            "beats": [
                "첫 시선이 닿는 순간을 그린다",
                "서로의 비밀을 나누며 유대감을 키운다",
                "시험이 둘의 의지를 점검한다",
                "감정과 의무가 충돌한다",
                "새로운 약속으로 결말을 맺는다"
            ],
            "color": "금빛 로즈",
            "imagery": [
                "빛나는 마법 서약",
                "공중에 떠 있는 장미 꽃잎",
                "성벽 위에서 맞잡은 손",
                "별빛이 떨어지는 무도회"
            ]
        }
    }

    # English runtime copy. Keeping all player-facing narrative content in one
    # data block prevents mixed-language procedural fallbacks.
    MBTI_BRIEF = {
        "I": "introspective and thoughtful", "E": "outgoing and relationship-oriented",
        "N": "guided by intuition and insight", "S": "attentive to concrete details",
        "T": "drawn to logic and structure", "F": "guided by empathy and emotion",
        "J": "organized and deliberate", "P": "flexible and spontaneous",
        "X": "open to exploring different traits"
    }
    ACT_STRUCTURE = [
        {"key": "origin", "title": "Origin", "intent": "Establish the beginning of the journey.", "question": "Why did this journey begin?"},
        {"key": "growth", "title": "Growth", "intent": "Expand the world and its relationships.", "question": "What new connection changes the path?"},
        {"key": "crisis", "title": "Crisis", "intent": "Bring the central conflict to its breaking point.", "question": "What is the greatest obstacle?"},
        {"key": "climax", "title": "Climax", "intent": "Set the direction through a decisive choice.", "question": "Who prevails, and what must be sacrificed?"},
        {"key": "resolution", "title": "Resolution", "intent": "Resolve the meaning of the journey.", "question": "What do these choices ultimately mean?"}
    ]
    GENRE_FLAVORS = {
        "mystery": {
            "label": "Mystery",
            "settings": ["a rain-soaked alley", "the library of a sealed manor", "a fog-covered bridge", "a shadowed harbor", "a silent cemetery"],
            "verbs": ["Trace", "Decode", "Capture", "Ambush", "Observe"],
            "twists": ["a hidden note surfaces", "a witness reverses their testimony", "an alibi collapses", "the same symbol appears again", "the power suddenly fails", "someone's footprints disappear"],
            "beats": ["uncover a hidden motive", "collect an impossible clue", "pressure a suspicious figure", "face the conflict between truth and fear", "decide whether to reveal or bury the secret"],
            "color": "deep teal", "imagery": ["a silhouette beneath a streetlamp", "a riverbank swallowed by fog", "a locked secret door", "a clue board bound in red thread"]
        },
        "cyberpunk": {
            "label": "Cyberpunk",
            "settings": ["a neon high-rise district", "a compromised data lounge", "a megacorp security room", "an illegal augmentation clinic", "a digital backstreet"],
            "verbs": ["Infiltrate", "Rewrite", "Analyze", "Augment", "Synchronize"],
            "twists": ["an AI speaks through a hidden channel", "the firewall opens by itself", "an unidentified human drone joins the chase", "reality begins to resemble a simulation", "the target has already changed bodies", "a memory-editing log is restored"],
            "beats": ["find the city's hidden backdoor", "learn what the connected strangers want", "balance data against emotion", "confront a fracture in identity", "define a new protocol"],
            "color": "neon magenta", "imagery": ["a luminous augmented arm", "hovercars crossing above the city", "data rain over the skyline", "light leaking from a bionic eye"]
        },
        "sf": {
            "label": "Science Fiction",
            "settings": ["an orbital briefing room", "an interplanetary communications hub", "the heart of an energy core", "the surface of an unknown planet", "a deep-space probe"],
            "verbs": ["Analyze", "Explore", "Negotiate", "Redesign", "Predict"],
            "twists": ["an alien signal contains a mathematical plea", "a gravity anomaly responds to questions", "a crew member remembers the time loop", "the navigation AI admits it is learning emotions", "the entire planet is alive", "a parallel self transmits a warning"],
            "beats": ["balance curiosity with survival", "read the interests behind interstellar politics", "test an unpredictable phenomenon", "prepare for first contact", "choose the next direction of exploration"],
            "color": "silver dawn", "imagery": ["a ship suspended beneath the stars", "a face reflected in a transparent interface", "a panorama of impossible terrain", "an orbital city held aloft by magnetism"]
        },
        "romance": {
            "label": "Romance Fantasy",
            "settings": ["the corridor of a magic academy", "a hidden palace garden", "a moonlit library", "a ballroom on a floating island", "a greenhouse beneath a glass dome"],
            "verbs": ["Confront", "Resonate with", "Confess to", "Rewrite fate beside", "Exchange a vow with"],
            "twists": ["a sealed spell awakens", "a symbol of fate begins to glow", "time stops around the two of them", "a hidden bloodline is revealed", "their fragments of memory call to each other", "the floating island tests their bond"],
            "beats": ["capture the instant their eyes first meet", "deepen trust through shared secrets", "let a trial test their resolve", "set emotion against duty", "close with a new promise"],
            "color": "golden rose", "imagery": ["a glowing magical vow", "rose petals suspended in the air", "hands joined atop a castle wall", "a ballroom beneath falling starlight"]
        }
    }

    FALLBACK_ACTIONS = {
        "mystery": ["Follow the clue", "Question the witness", "Protect the evidence"],
        "cyberpunk": ["Breach the network", "Trust the rogue signal", "Rewrite the protocol"],
        "sf": ["Investigate the anomaly", "Contact the unknown", "Protect the crew"],
        "romance": ["Reveal the secret", "Defy the prophecy", "Make a promise"]
    }

    SOUNDTRACK_LIBRARY = {
        "mystery": [
            {"act_key": "origin", "title": "Misty Alley Echo", "api": "Pixabay", "file": "audio/mystery_origin.ogg"},
            {"act_key": "growth", "title": "Clue Patterns", "api": "Pixabay", "file": "audio/mystery_growth.ogg"},
            {"act_key": "crisis", "title": "Shadowed Countdown", "api": "Pixabay", "file": "audio/mystery_crisis.ogg"},
            {"act_key": "climax", "title": "Truth Burst", "api": "Pixabay", "file": "audio/mystery_climax.ogg"},
            {"act_key": "resolution", "title": "Quiet Revelation", "api": "Pixabay", "file": "audio/mystery_resolution.ogg"}
        ],
        "cyberpunk": [
            {"act_key": "origin", "title": "Neon Boot Sequence", "api": "Pixabay", "file": "audio/cyberpunk_origin.ogg"},
            {"act_key": "growth", "title": "Chrome Tension", "api": "Pixabay", "file": "audio/cyberpunk_growth.ogg"},
            {"act_key": "crisis", "title": "Firewall Breach", "api": "Pixabay", "file": "audio/cyberpunk_crisis.ogg"},
            {"act_key": "climax", "title": "Overclocked Fate", "api": "Pixabay", "file": "audio/cyberpunk_climax.ogg"},
            {"act_key": "resolution", "title": "Synth Dawn", "api": "Pixabay", "file": "audio/cyberpunk_resolution.ogg"}
        ],
        "sf": [
            {"act_key": "origin", "title": "Orbital Prelude", "api": "Pixabay", "file": "audio/sf_origin.ogg"},
            {"act_key": "growth", "title": "Vector Drift", "api": "Pixabay", "file": "audio/sf_growth.ogg"},
            {"act_key": "crisis", "title": "Gravity Surge", "api": "Pixabay", "file": "audio/sf_crisis.ogg"},
            {"act_key": "climax", "title": "Singularity Call", "api": "Pixabay", "file": "audio/sf_climax.ogg"},
            {"act_key": "resolution", "title": "Stellar Echo", "api": "Pixabay", "file": "audio/sf_resolution.ogg"}
        ],
        "romance": [
            {"act_key": "origin", "title": "Petals Awaken", "api": "Pixabay", "file": "audio/romance_origin.ogg"},
            {"act_key": "growth", "title": "Moonlit Promise", "api": "Pixabay", "file": "audio/romance_growth.ogg"},
            {"act_key": "crisis", "title": "Heart Trial", "api": "Pixabay", "file": "audio/romance_crisis.ogg"},
            {"act_key": "climax", "title": "Destined Embrace", "api": "Pixabay", "file": "audio/romance_climax.ogg"},
            {"act_key": "resolution", "title": "Eternal Bloom", "api": "Pixabay", "file": "audio/romance_resolution.ogg"}
        ],
        "default": [
            {"act_key": "origin", "title": "Opening Pulse", "api": "Pixabay", "file": None},
            {"act_key": "growth", "title": "Expanding Paths", "api": "Pixabay", "file": None},
            {"act_key": "crisis", "title": "Crossroad Tension", "api": "Pixabay", "file": None},
            {"act_key": "climax", "title": "Turning Point", "api": "Pixabay", "file": None},
            {"act_key": "resolution", "title": "New Horizon", "api": "Pixabay", "file": None}
        ],
        "ending": [
            {"act_key": "ending", "title": "Keepsake Outro", "api": "Pixabay", "file": "audio/ending_theme.ogg"}
        ]
    }

    class StorySession(object):
        def __init__(self):
            self.total_acts = len(ACT_STRUCTURE)
            self.session_count = 0
            self.reset()

        def reset(self):
            self.profile = {}
            self.genre = "mystery"
            self.start_sentence = ""
            self.choices = []
            self.soundtrack_log = []
            self.session_seed = random.randint(1, 10_000_000)
            self.choice_rng = random.Random(self.session_seed)
            self.current_act_index = 0
            self.music_enabled = True
            self.active_track = None
            self.ai_mode = "checking"
            self.ai_model = None
            self.last_ai_error = None
            self.illustration_status = "idle"
            self.illustration_context = None
            self.illustration_path = None
            self.illustration_displayable = None
            self.illustration_model = None
            self.illustration_credits = 0
            self.illustration_cached = False
            self.illustration_error = None
            self.archive_dir = None
            self.archive_story_path = None
            self.archive_manifest_path = None
            self.archive_error = None

        def prepare_session(self, profile, genre, start_sentence):
            self.reset()
            genre_key = genre if genre in GENRE_FLAVORS else "mystery"
            profile = dict(profile)
            profile.setdefault("style", "layered")
            profile.setdefault("mood", "reflective")
            profile.setdefault("protagonist_name", "Player")
            mbti_code = normalize_mbti(profile.get("mbti"))
            profile["mbti"] = mbti_code
            profile["mbti_expanded"] = self._expand_mbti(mbti_code)
            profile["genre_label"] = GENRE_FLAVORS[genre_key]["label"]
            self.profile = profile
            self.genre = genre_key
            self.start_sentence = start_sentence.strip() if start_sentence else ""
            composite_seed = f"{self.session_seed}-{genre_key}-{profile['mbti']}-{self.start_sentence}"
            self.choice_rng.seed(composite_seed)
            self.current_act_index = 0
            self.soundtrack_log = []
            self.active_track = None
            self.music_enabled = True
            return self

        def get_act_data(self):
            return ACT_STRUCTURE[self.current_act_index]

        def build_act_intro(self):
            act_data = self.get_act_data()
            flavor = GENRE_FLAVORS[self.genre]
            beat = cycle_pick(flavor["beats"], self.current_act_index)
            return f"{act_data['title']} - {beat.capitalize()}. {act_data['intent']}"

        def generate_choices(self):
            act_data = self.get_act_data()
            flavor = GENRE_FLAVORS[self.genre]
            ai_choices = self._generate_ai_choices(act_data, flavor)
            if ai_choices:
                return ai_choices
            variants = []
            actions = FALLBACK_ACTIONS.get(self.genre, ["Take the risk", "Seek the truth", "Protect what matters"])
            for idx in range(3):
                anchor = cycle_pick(flavor["settings"], self.current_act_index + idx + self.session_seed)
                action = cycle_pick(actions, self.current_act_index + idx + self.session_seed)
                twist = cycle_pick(flavor["twists"], self.current_act_index * 5 + idx * 2 + self.session_seed)
                headline = f"{action} at {anchor}"
                detail = f"Choose this path as {twist}; the decision will shape what happens next."
                narrative = self._craft_narrative(act_data, anchor, action, twist)
                impact = self._craft_impact(act_data, twist)
                variants.append({
                    "headline": headline,
                    "detail": detail,
                    "narrative": narrative,
                    "impact": impact,
                    "act_key": act_data["key"],
                    "act_title": act_data["title"]
                })
            return variants

        def _generate_ai_choices(self, act_data, flavor):
            """Ask the local key-holding proxy for choices, then fail closed."""
            payload = {
                "profile": self.profile,
                "genre": self.genre,
                "genre_label": flavor["label"],
                "opening_sentence": self.start_sentence,
                "act": act_data,
                "previous_choices": [
                    {
                        "headline": item.get("headline", ""),
                        "narrative": item.get("narrative", ""),
                        "impact": item.get("impact", "")
                    }
                    for item in self.choices
                ]
            }
            try:
                request = urllib.request.Request(
                    STORY_API_URL,
                    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                response = urllib.request.urlopen(request, timeout=30)
                result = json.loads(response.read().decode("utf-8"))
                choices = result.get("choices", [])
                required = ("headline", "detail", "narrative", "impact")
                if len(choices) != 3:
                    raise ValueError("AI response did not contain exactly three choices")
                validated = []
                for item in choices:
                    if not all(isinstance(item.get(key), str) and item[key].strip() for key in required):
                        raise ValueError("AI choice is missing a required text field")
                    clean = {
                        "headline": safe_generated_text(item["headline"], 100),
                        "detail": safe_generated_text(item["detail"], 240),
                        "narrative": safe_generated_text(item["narrative"], 900),
                        "impact": safe_generated_text(item["impact"], 300)
                    }
                    clean["act_key"] = act_data["key"]
                    clean["act_title"] = act_data["title"]
                    validated.append(clean)
                self.ai_mode = "online"
                self.ai_model = result.get("model", "gpt-5.6-luna")
                self.last_ai_error = None
                return validated
            except Exception as exc:
                self.ai_mode = "offline"
                self.ai_model = None
                self.last_ai_error = str(exc)[:160]
                return None

        def begin_act(self):
            act_key = self.get_act_data()["key"]
            track = self._resolve_track(act_key)
            if len(self.soundtrack_log) == self.current_act_index:
                self.soundtrack_log.append(track)
            else:
                self.soundtrack_log[self.current_act_index] = track
            if self.music_enabled:
                self._activate_track(track)
            return track

        def commit_choice(self, choice):
            chosen = dict(choice)
            chosen["act_index"] = self.current_act_index
            self.choices.append(chosen)
            self.current_act_index += 1

        def _build_context_phrase(self, act_data):
            pieces = []
            mbti_label = self.profile.get("mbti_expanded")
            if mbti_label:
                pieces.append(mbti_label)
            style = self.profile.get("style")
            if style:
                pieces.append(f"style: {style}")
            mood = self.profile.get("mood")
            if mood:
                pieces.append(f"mood: {mood}")
            last_headline = self.choices[-1]["headline"] if self.choices else None
            summary = " | ".join(pieces)
            if last_headline:
                summary += f"; the consequences of '{last_headline}' still linger"
            return summary if summary else act_data["intent"]

        def _craft_narrative(self, act_data, anchor, action, twist):
            flavor = GENRE_FLAVORS[self.genre]
            mood = self.profile.get("mood", "a complicated state of mind")
            protagonist = self.profile.get("protagonist_name", "the protagonist")
            opening = f"During the {act_data['title'].lower()}, {protagonist} chooses to {action.lower()} at {anchor}."
            texture = f"The {flavor['color']} atmosphere tightens around a feeling of {mood}."
            payoff = f"The choice changes the course of the story when {twist}."
            return " ".join([opening, texture, payoff])

        def _craft_impact(self, act_data, twist):
            return f"Consequence: {twist.capitalize()}. The next act begins with that change still in motion."

        def _resolve_track(self, act_key):
            catalog = SOUNDTRACK_LIBRARY.get(self.genre, [])
            fallback = SOUNDTRACK_LIBRARY.get("default", [])
            for item in catalog:
                if item["act_key"] == act_key:
                    return self._track_with_availability(item)
            for item in fallback:
                if item["act_key"] == act_key:
                    return self._track_with_availability(item)
            return self._track_with_availability({
                "act_key": act_key,
                "title": f"{self.genre.title()} Placeholder",
                "api": "Pixabay",
                "file": None
            })

        def _track_with_availability(self, data):
            file_path = data.get("file")
            available = bool(file_path and renpy.loader.loadable(file_path))
            return {
                "act_key": data.get("act_key"),
                "title": data.get("title"),
                "source_api": data.get("api"),
                "file": file_path if available else None,
                "available": available
            }

        def _activate_track(self, track):
            if track["file"]:
                renpy.music.play(track["file"], channel="bgm", loop=True, fadein=0.6)
            else:
                renpy.music.stop(channel="bgm")
            self.active_track = track

        def toggle_music(self):
            self.music_enabled = not self.music_enabled
            if self.music_enabled:
                if self.soundtrack_log:
                    self._activate_track(self.soundtrack_log[min(self.current_act_index, len(self.soundtrack_log) - 1)])
            else:
                renpy.music.stop(channel="bgm")

        def compose_finale(self):
            story_lines = []
            if self.start_sentence:
                story_lines.append(self.start_sentence)
            for choice in self.choices:
                story_lines.append(choice["narrative"])
            epilogue = self._build_epilogue()
            story_lines.append(epilogue)
            wrapped = [textwrap.fill(line, 72) for line in story_lines]
            illustration_prompt = self._build_illustration_prompt(epilogue)
            self.illustration_context = self._build_illustration_context(epilogue, illustration_prompt)
            self.illustration_status = "idle"
            self.illustration_path = None
            self.illustration_displayable = None
            self.illustration_model = None
            self.illustration_credits = 0
            self.illustration_cached = False
            self.illustration_error = None
            soundtrack_summary = self._soundtrack_summary()
            self.session_count += 1
            payload = {
                "story": "\n\n".join(wrapped),
                "illustration_prompt": illustration_prompt,
                "soundtrack": soundtrack_summary
            }
            try:
                self._create_story_archive(payload, epilogue)
                self.archive_error = None
            except Exception as exc:
                self.archive_dir = None
                self.archive_story_path = None
                self.archive_manifest_path = None
                self.archive_error = str(exc)[:240]
            return payload

        def _create_story_archive(self, payload, epilogue):
            """Persist every completed playthrough before optional image generation."""
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            session_id = "{}-{}".format(timestamp, str(self.session_seed)[-6:])
            root = os.path.join(renpy.config.savedir, "story_archive")
            archive_dir = os.path.join(root, session_id)
            suffix = 1
            while os.path.exists(archive_dir):
                archive_dir = os.path.join(root, "{}-{}".format(session_id, suffix))
                suffix += 1
            os.makedirs(archive_dir)
            self.archive_dir = archive_dir
            self.archive_story_path = os.path.join(archive_dir, "story.txt")
            self.archive_manifest_path = os.path.join(archive_dir, "session.json")
            with open(self.archive_story_path, "w", encoding="utf-8") as story_file:
                story_file.write("You Can Be Anything\n")
                story_file.write("=" * 24 + "\n\n")
                story_file.write(payload["story"])
                story_file.write("\n\nIllustration Prompt\n-------------------\n")
                story_file.write(payload["illustration_prompt"])
                story_file.write("\n\nSoundtrack\n----------\n")
                story_file.write(payload["soundtrack"])
                story_file.write("\n")
            manifest = {
                "archive_version": 1,
                "created_at": datetime.datetime.now().isoformat(),
                "profile": self.profile,
                "genre": self.genre,
                "opening_sentence": self.start_sentence,
                "choices": self.choices,
                "epilogue": epilogue,
                "story": payload["story"],
                "illustration_prompt": payload["illustration_prompt"],
                "soundtrack": payload["soundtrack"],
                "illustration": None
            }
            self._write_archive_manifest(manifest)

        def _write_archive_manifest(self, manifest):
            temporary = self.archive_manifest_path + ".tmp"
            with open(temporary, "w", encoding="utf-8") as manifest_file:
                json.dump(manifest, manifest_file, ensure_ascii=False, indent=2)
            os.replace(temporary, self.archive_manifest_path)

        def _attach_illustration_to_archive(self, result):
            if not self.archive_dir or not self.archive_manifest_path:
                return
            destination = os.path.join(self.archive_dir, "illustration.png")
            if os.path.abspath(result["image_path"]) != os.path.abspath(destination):
                shutil.copy2(result["image_path"], destination)
            with open(self.archive_manifest_path, "r", encoding="utf-8") as manifest_file:
                manifest = json.load(manifest_file)
            manifest["illustration"] = {
                "file": "illustration.png",
                "model": result.get("model", "gpt-image-1-mini"),
                "quality": "low",
                "cached": bool(result.get("cached", False)),
                "estimated_credits": int(result.get("credits", 0))
            }
            self._write_archive_manifest(manifest)

        def _build_illustration_context(self, epilogue, visual_hint):
            """Create a bounded, serializable final-state payload for image generation."""
            return {
                "profile": {
                    "protagonist_name": self.profile.get("protagonist_name", "Protagonist"),
                    "mbti": self.profile.get("mbti", ""),
                    "mbti_expanded": self.profile.get("mbti_expanded", ""),
                    "style": self.profile.get("style", ""),
                    "mood": self.profile.get("mood", "")
                },
                "genre": self.genre,
                "genre_label": self.profile.get("genre_label", ""),
                "opening_sentence": self.start_sentence,
                "choices": [
                    {
                        "headline": choice.get("headline", ""),
                        "impact": choice.get("impact", "")
                    }
                    for choice in self.choices
                ],
                "epilogue": epilogue,
                "visual_hint": visual_hint
            }

        def start_illustration(self):
            if self.illustration_status in ("generating", "completed"):
                return
            if not self.illustration_context:
                self.illustration_status = "failed"
                self.illustration_error = "The finale data is not ready."
                return
            self.illustration_status = "generating"
            self.illustration_error = None
            renpy.invoke_in_thread(self._illustration_worker, dict(self.illustration_context))

        def _illustration_worker(self, context):
            try:
                try:
                    health_response = urllib.request.urlopen(STORY_API_HEALTH_URL, timeout=3)
                    health = json.loads(health_response.read().decode("utf-8"))
                    if not health.get("ok"):
                        raise ValueError("The local AI proxy did not report a ready state.")
                except Exception as exc:
                    raise RuntimeError("The local AI proxy is not running on port 8765. Start it before generating an illustration.") from exc
                request = urllib.request.Request(
                    ILLUSTRATION_API_URL,
                    data=json.dumps(context, ensure_ascii=False).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                response = urllib.request.urlopen(request, timeout=210)
                result = json.loads(response.read().decode("utf-8"))
                if not result.get("ok") or not result.get("image_path"):
                    raise ValueError("The image server did not return a completed file.")
                renpy.invoke_in_main_thread(self._finish_illustration, result, None)
            except Exception as exc:
                renpy.invoke_in_main_thread(self._finish_illustration, None, self._friendly_illustration_error(exc))

        def _friendly_illustration_error(self, exc):
            message = str(exc)
            lowered = message.lower()
            if "10061" in message or "connection refused" in lowered or "port 8765" in lowered:
                return "The local AI proxy is not running. Start the proxy, then return here and try again. No image request reached the proxy."
            if "timed out" in lowered or "timeout" in lowered:
                return "The image request timed out. Check the proxy log before deciding whether to retry, because the provider may have received it."
            if "already running" in lowered:
                return "An illustration request for this ending is already running. Wait for it to finish instead of submitting another request."
            if "http error 401" in lowered or "http 401" in lowered:
                return "The proxy rejected the credential. Check the external credential file; do not copy it into the game folder."
            if "http error 429" in lowered or "http 429" in lowered:
                return "The image service rate limit or credit limit was reached. Check the proxy log before retrying."
            return "Image generation failed. Check the local proxy log before retrying. Details: {}".format(message[:160])

        def _finish_illustration(self, result, error):
            if error:
                self.illustration_status = "failed"
                self.illustration_error = error
            else:
                try:
                    self.illustration_path = result["image_path"]
                    with open(self.illustration_path, "rb") as image_file:
                        image_bytes = image_file.read()
                    self.illustration_displayable = im.Data(image_bytes, "generated_illustration.png")
                    self.illustration_model = result.get("model", "gpt-image-1-mini")
                    self.illustration_credits = int(result.get("credits", 0))
                    self.illustration_cached = bool(result.get("cached", False))
                    self._attach_illustration_to_archive(result)
                    self.illustration_status = "completed"
                    self.illustration_error = None
                except Exception as exc:
                    self.illustration_status = "failed"
                    self.illustration_error = str(exc)[:240]
            renpy.restart_interaction()

        def illustration_cost_label(self):
            if self.illustration_cached:
                return "Cached | 0 additional credits"
            return "Estimated request cost: {} credits".format(self.illustration_credits)

        def illustration_summary(self):
            return "{} | {}".format(self.illustration_model or "gpt-image-1-mini", self.illustration_cost_label())

        def archive_label(self):
            if self.archive_dir:
                return "Playthrough saved to: {}".format(self.archive_dir)
            if self.archive_error:
                return "Could not save playthrough: {}".format(self.archive_error)
            return "Playthrough archive is not available."

        def genre_status_label(self):
            return "Genre: {}".format(self.profile.get("genre_label", ""))

        def ai_status_label(self):
            if self.ai_mode == "online":
                return "Choices: AI | {}".format(self.ai_model or "gpt-5.6-luna")
            if self.ai_mode == "offline":
                return "Choices: offline generator"
            return "Choices: checking AI connection"

        def act_choice_title(self, act_title):
            return "{} Choice".format(act_title)

        def _build_epilogue(self):
            flavor = GENRE_FLAVORS[self.genre]
            headline = self.choices[-1]["headline"] if self.choices else "an unknown choice"
            resonance = f"A {self.profile.get('style', 'layered')} sensibility shapes the final moment."
            replay_hint = "Different choices can open an entirely different ending."
            return f"In the fading atmosphere of {flavor['label']}, the decision to '{headline}' brings every piece together. {resonance} {replay_hint}"

        def _build_illustration_prompt(self, epilogue):
            flavor = GENRE_FLAVORS[self.genre]
            traits = [
                self.profile.get("mbti_expanded"),
                self.profile.get("style"),
                self.profile.get("mood")
            ]
            traits = [t for t in traits if t]
            trait_text = ", ".join(traits) if traits else "a layered atmosphere"
            imagery = cycle_pick(flavor["imagery"], self.session_count)
            return f"A {flavor['label']} finale featuring {trait_text} and {imagery}. Key moment: {epilogue}"

        def _soundtrack_summary(self):
            summary_lines = []
            for idx, track in enumerate(self.soundtrack_log):
                if idx < len(ACT_STRUCTURE):
                    act_title = ACT_STRUCTURE[idx]["title"]
                else:
                    act_title = f"Act {idx + 1}"
                status = "available" if track["available"] else "not bundled"
                summary_lines.append(f"{act_title}: {track['title']} ({track['source_api']} | {status})")
            ending_list = SOUNDTRACK_LIBRARY.get("ending", [])
            if ending_list:
                ending_track = self._track_with_availability(ending_list[0])
                status = "available" if ending_track["available"] else "not bundled"
                summary_lines.append(f"Ending: {ending_track['title']} ({ending_track['source_api']} | {status})")
            return "\n".join(summary_lines)

        def _expand_mbti(self, code):
            descriptors = [MBTI_BRIEF.get(letter, "") for letter in code]
            descriptors = [d for d in descriptors if d]
            return ", ".join(descriptors)

        def overlay_summary(self):
            return f"{self.profile.get('mbti', '----')} | {self.profile.get('style', '')} | {self.profile.get('mood', '')}".strip()

        def profile_summary(self):
            return "Profile: {} / {} / {} / {}".format(
                self.profile.get("protagonist_name", "Protagonist"),
                self.profile.get("mbti", "----"),
                self.profile.get("style", ""),
                self.profile.get("mood", "")
            )

        def progress_label(self):
            current = min(self.current_act_index + 1, self.total_acts)
            return f"{current}/{self.total_acts}"

        def current_act_number(self):
            if self.current_act_index >= self.total_acts:
                return self.total_acts
            return self.current_act_index + 1
    story_state = StorySession()

    def reset_story_session():
        story_state.reset()

define narrator = Character(None)


label profile_setup:
    $ protagonist_name = renpy.input("Enter the protagonist's name (defaults to 'Player'):", default="Player").strip()
    $ mbti = renpy.input("Enter an MBTI type (for example, INFP):", default=story_state.profile.get("mbti", "INFP")).strip()
    $ style = renpy.input("Enter a preferred style keyword (for example, cinematic):", default=story_state.profile.get("style", "cinematic")).strip()
    $ mood = renpy.input("Describe the protagonist's current mood:", default=story_state.profile.get("mood", "curious")).strip()
    $ genre = story_state.genre or "mystery"
    narrator "Which genre would you like to explore?"

    menu genre_select:
        "Mystery":
            $ genre = "mystery"
        "Cyberpunk":
            $ genre = "cyberpunk"
        "SF":
            $ genre = "sf"
        "Romance Fantasy":
            $ genre = "romance"
    $ default_sentence = "When I opened my eyes, a black lake stretched before me."
    $ start_sentence = renpy.input("Write an opening sentence for the story:", default=story_state.start_sentence or default_sentence).strip()
    if not start_sentence:
        $ start_sentence = default_sentence
    $ profile = {
        "protagonist_name": protagonist_name or "Player",
        "mbti": mbti or "INFP",
        "style": style or "cinematic",
        "mood": mood or "curious"
    }
    $ story_state.prepare_session(profile, genre, start_sentence)
    return


label start:
    scene black
    with fade

    call profile_setup

    narrator "You are [story_state.profile.get('protagonist_name', 'the protagonist')], [story_state.profile.get('mbti_expanded', 'a person of many possibilities')]."
    narrator "Your genre is [story_state.profile.get('genre_label', 'Mystery')], and your story begins: \"[story_state.start_sentence]\""

    show screen story_overlay

    while story_state.current_act_index < story_state.total_acts:
        $ story_state.begin_act()
        $ act_data = story_state.get_act_data()
        $ act_intro = story_state.build_act_intro()
        narrator "[act_intro]"
        $ choices = story_state.generate_choices()
        $ selection = renpy.call_screen("act_choice_screen", act_title=act_data["title"], act_intro=act_intro, choices=choices)
        if selection is None:
            $ selection = choices[0]
        $ story_state.commit_choice(selection)
        $ selected_narrative = selection.get("narrative", "Your decision changes the path ahead.")
        $ selected_impact = selection.get("impact", "Its consequences carry into the next act.")
        narrator "[selected_narrative]"
        narrator "[selected_impact]"

    hide screen story_overlay
    $ renpy.music.stop(channel="bgm")
    $ finale_payload = story_state.compose_finale()
    $ decision = "menu"
    $ decision = renpy.call_screen("finale_screen", story=finale_payload["story"], illustration_prompt=finale_payload["illustration_prompt"], soundtrack=finale_payload["soundtrack"], profile=story_state.profile)

    if decision == "replay":
        jump start
    else:
        return


screen story_overlay():
    zorder 100
    if story_state.total_acts:
        frame:
            align (0.02, 0.02)
            has vbox
            spacing 6
            text "Profile" size 32
            text story_state.overlay_summary() size 24
            text story_state.genre_status_label() size 22
            if story_state.ai_mode == "online":
                text story_state.ai_status_label() size 20 color "#8fe3a5"
            elif story_state.ai_mode == "offline":
                text story_state.ai_status_label() size 20 color "#ffd27f"
            else:
                text story_state.ai_status_label() size 20
        frame:
            align (0.98, 0.02)
            has vbox
            spacing 6
            text story_state.progress_label() size 28
            bar value story_state.current_act_index range story_state.total_acts xmaximum 260
            if story_state.active_track:
                text story_state.active_track.get("title", "") size 22
                text story_state.active_track.get("source_api", "") size 20
            textbutton ("Mute BGM" if story_state.music_enabled else "Enable BGM") action Function(story_state.toggle_music) xalign 1.0


screen act_choice_screen(act_title, act_intro, choices):
    tag menu
    modal True
    add Solid("#0008")
    frame:
        xalign 0.5
        yalign 0.5
        xmaximum 1200
        ymaximum 680
        padding (40, 30)
        has vbox
        spacing 24
        text story_state.act_choice_title(act_title) size 42
        text act_intro size 26
        viewport:
            draggable True
            mousewheel True
            scrollbars "vertical"
            ymaximum 420
            frame:
                padding (0, 0)
                has vbox
                spacing 18
                for choice in choices:
                    textbutton choice["headline"] action Return(choice) text_size 28 xfill True
                    text choice["detail"] size 22 substitute False


screen finale_screen(story, illustration_prompt, soundtrack, profile):
    tag menu
    modal True
    add Solid("#0008")
    frame:
        xalign 0.5
        yalign 0.5
        xmaximum 1100
        ymaximum 700
        padding (40, 30)
        has vbox
        spacing 16
        viewport:
            draggable True
            mousewheel True
            scrollbars "vertical"
            ymaximum 560
            has vbox
            spacing 18
            text "Completed Story" size 44
            text story_state.profile_summary() size 24
            frame:
                padding (10, 10)
                background Solid("#1116")
                text story size 24
            text "Finale Illustration Prompt" size 30
            frame:
                padding (10, 10)
                background Solid("#1116")
                text illustration_prompt size 24
            if story_state.illustration_status == "idle":
                textbutton "Generate Protagonist Illustration - up to 8 credits":
                    action Confirm("Generate one low-quality finale illustration? This may use up to 8 credits.", Function(story_state.start_illustration))
                    xalign 0.5
            elif story_state.illustration_status == "generating":
                text "Generating the illustration... The button is locked to prevent duplicate requests." size 24 color "#ffd27f" xalign 0.5
            elif story_state.illustration_status == "completed":
                text "Generated Protagonist Illustration" size 30
                if story_state.illustration_displayable:
                    add Transform(story_state.illustration_displayable, fit="contain", xsize=960, ysize=540) xalign 0.5
                text story_state.illustration_summary() size 22 xalign 0.5 color "#8fe3a5"
                text story_state.archive_label() size 18 xalign 0.5
            elif story_state.illustration_status == "failed":
                text "Illustration generation failed. It was not retried automatically." size 24 color "#ff9f9f" xalign 0.5
                text story_state.illustration_error size 18 xalign 0.5 substitute False
                textbutton "Retry Manually - up to 8 credits":
                    action Confirm("Check whether the previous request was charged before retrying. Continue?", Function(story_state.start_illustration))
                    xalign 0.5
            text "Soundtrack" size 30
            frame:
                padding (10, 10)
                background Solid("#1116")
                text soundtrack size 24
            text story_state.archive_label() size 18 xalign 0.5 color "#8fe3a5"
        hbox:
            spacing 40
            xalign 0.5
            textbutton "Try Another Path" action Return("replay")
            textbutton "Main Menu" action Return("menu")
