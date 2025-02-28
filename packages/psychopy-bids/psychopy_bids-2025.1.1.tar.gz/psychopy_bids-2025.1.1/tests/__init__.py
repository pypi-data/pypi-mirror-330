import importlib.metadata

if not hasattr(importlib.metadata.PathDistribution, "name"):
    setattr(
        importlib.metadata.PathDistribution,
        "name",
        property(lambda self: str(self._path)),
    )
