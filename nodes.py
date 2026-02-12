# nodes.py — ComfyUI-TextJoinZveroboy
# - text_1/text_2 are OPTIONAL (so workflow runs even if text_1 is not connected)
# - accepts dynamically created inputs text_3, text_4, ... via ContainsAnyDict + **kwargs [page:1]

class ContainsAnyDict(dict):
    def __contains__(self, key):
        return True

    def __getitem__(self, key):
        return dict.get(self, key)


def _as_nonempty_str(v):
    if v is None:
        return None
    s = str(v)
    if s.strip() == "":
        return None
    return s


class TextJoinZveroboy:
    @classmethod
    def INPUT_TYPES(cls):
        opt = ContainsAnyDict()

        # Base inputs: optional, but default to ports
        opt["text_1"] = ("STRING", {"default": "", "multiline": True, "forceInput": True})
        opt["text_2"] = ("STRING", {"default": "", "multiline": True, "forceInput": True})

        # Any client-created inputs (text_3, text_4, ...) will also be accepted because of ContainsAnyDict [page:1]
        return {
            "required": {
                "separator": ("STRING", {"default": ""}),
            },
            "optional": opt,
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "join"
    CATEGORY = "Zveroboy/Text"

    def join(self, separator="", text_1=None, text_2=None, **kwargs):
        # Collect fixed optional inputs
        values = [text_1, text_2]

        # Collect dynamic inputs text_3..text_n from kwargs (created by JS on client)
        dyn_keys = [k for k in kwargs.keys() if isinstance(k, str) and k.startswith("text_")]

        def _key_num(k: str):
            try:
                return int(k.split("_", 1)[1])
            except Exception:
                return 10**9

        for k in sorted(dyn_keys, key=_key_num):
            values.append(kwargs.get(k))

        # Filter out empty values
        parts = []
        for v in values:
            s = _as_nonempty_str(v)
            if s is not None:
                parts.append(s)

        return (separator.join(parts) if parts else "",)


NODE_CLASS_MAPPINGS = {
    "TextJoinZveroboy": TextJoinZveroboy,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextJoinZveroboy": "Text Join (Zveroboy)",
}
