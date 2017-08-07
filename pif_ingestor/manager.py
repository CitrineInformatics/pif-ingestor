import stevedore
import logging


def callback(manager, entrypoint, exception):
    """Log errors in loading extensions as warnings"""
    logging.warning("Failed to load '{}' due to {}".format(entrypoint, exception))
    return


def run_extension(name, path, args):
    """Run extension by name on path with arguments"""
    # Load extensions
    mgr = stevedore.extension.ExtensionManager(
        namespace='citrine.dice.converter',
        invoke_on_load=False,
        on_load_failure_callback=callback
    )

    if name in mgr:
        extension = mgr[name]
        pifs = extension.plugin.convert([path], **args)
        return pifs
    else:
        logging.error("{} is an unknown format\nAvailable formats: {}".format(name, mgr.names()))
        exit(1)
