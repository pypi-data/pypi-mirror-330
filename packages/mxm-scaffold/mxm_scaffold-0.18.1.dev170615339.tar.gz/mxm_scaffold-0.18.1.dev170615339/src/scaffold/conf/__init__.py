def register_all() -> None:
    """All @structured_config classes register themselves when imported / defined"""
    from scaffold.conf.scaffold import artifact_manager  # noqa:F401
    from scaffold.conf.scaffold import entrypoint  # noqa:F401

    try:
        from scaffold.conf.scaffold import flyte_launcher  # noqa:F401
    except ModuleNotFoundError:
        # in case we didnt install flyte extra package
        pass
