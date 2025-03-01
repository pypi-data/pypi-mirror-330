"""A helper module to collect citations from a software package."""

from functools import wraps
import inspect
import logging
import sys

from citation_compass.docstring_utils import (
    extract_citation,
    extract_urls,
)

CITATION_REGISTRY_ALL = {}
CITATION_REGISTRY_USED = set()


def _get_full_name(obj):
    """Return the maximally qualified name of a thing.

    Parameters
    ----------
    obj : object
        The obj to get the name of.

    Returns
    -------
    str
        The fully qualified name of the thing.
    """
    # Try to determine the name of the "thing".
    if hasattr(obj, "__qualname__"):
        base_name = obj.__qualname__
    elif hasattr(obj, "__name__"):
        base_name = obj.__name__
    elif hasattr(obj, "__class__"):
        # If this is an object, use the class's name.
        base_name = obj.__class__.__qualname__
    else:
        raise ValueError(f"Could not determine the name of {obj}")

    # Get the string for the module (if we can find it).
    module = inspect.getmodule(obj)
    full_name = base_name if module is None else f"{module.__name__}.{base_name}"
    return full_name


class CitationEntry:
    """A (data)class to store information about a citation.

    Attributes
    ----------
    key : str
        The name of the module, function, or other aspect where the citation is needed.
    citation : str, optional
        The citation string.
    label : str, optional
        The (optional) user-defined label for the citation.
    urls : list of str
        A list of URLs extracted from the citation string.
    """

    def __init__(self, key, citation=None, label=None):
        self.key = key
        self.citation = citation
        self.label = label

        if citation is None:
            if label is not None and len(label) > 0:
                self.citation = label
            else:
                self.citation = "No citation provided."

        self.urls = extract_urls(self.citation)

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return f"{self.key}: {self.citation}"

    def __repr__(self):
        return f"{self.key}:\n{self.citation}"

    @classmethod
    def from_object(cls, obj, label=None):
        """Create a CitationEntry from any object (including a function or method).

        Parameters
        ----------
        obj : object
            The object from which to create the citation.
        label : str, optional
            The (optional) user-defined label for the citation.

        Returns
        -------
        CitationEntry
            The citation entry.
        """
        # Try to parse a citation from the object's docstring (if there is one).
        if hasattr(obj, "__doc__"):
            docstring = obj.__doc__
        elif hasattr(obj, "__class__") and hasattr(obj.__class__, "__doc__"):
            docstring = obj.__class__.__doc__
        else:
            docstring = ""
        citation_text = extract_citation(docstring)
        if citation_text is None:
            citation_text = docstring

        full_name = _get_full_name(obj)

        return cls(
            key=full_name,
            citation=citation_text,
            label=label,
        )


def cite_module(name, citation=None):
    """Add a citation to a entire module.

    Parameters
    ----------
    name : str
        The name of the module.
    citation : str, optional
        The citation string. If None the code automatically tries to extract the citation text
        from the module's docstring.
    """
    if citation is None and name in sys.modules:
        module = sys.modules[name]
        if hasattr(module, "__doc__"):
            citation = extract_citation(module.__doc__)
            if citation is None or len(citation) == 0:
                citation = module.__doc__

    CITATION_REGISTRY_ALL[name] = CitationEntry(name, citation)
    CITATION_REGISTRY_USED.add(name)


class CiteClass:
    """A super class for adding a citation to a class."""

    def __init__(self):
        pass

    def __init_subclass__(cls):
        # Add the class's full name
        full_name = _get_full_name(cls)
        cls._citation_compass_name = full_name

        # Save the citation as ALL when it is first defined.
        if full_name not in CITATION_REGISTRY_ALL:
            CITATION_REGISTRY_ALL[full_name] = CitationEntry.from_object(cls)
        else:
            logging.warning(f"Duplicated citation tag for class: {full_name}")

        # Wrap the constructor so the class is marked used when
        # the first object is instantiated.
        original_init = cls.__init__

        @wraps(original_init)
        def init_wrapper(*args, **kwargs):
            # Save the citation as USED when it is first called.
            if cls._citation_compass_name not in CITATION_REGISTRY_USED:
                CITATION_REGISTRY_USED.add(cls._citation_compass_name)
            return original_init(*args, **kwargs)

        cls.__init__ = init_wrapper


def cite_function(label=None, track_used=True):
    """A function wrapper for adding a citation to a function or
    class method.

    Parameters
    ----------
    label : str, optional
        The (optional) user-defined label for the citation.
    track_used : bool
        If True, the function will be marked as used when it is called.
        This adds a small amount of overhead to each function call.
        Default: True.

    Returns
    -------
    function
        The wrapped function or method.
    """
    # If the label is callable, there were no parentheses on the
    # dectorator and it passed in the function instead. So use None
    # as the label.
    use_label = label if not callable(label) else None

    def decorator(func):
        full_name = _get_full_name(func)

        # Save the citation as ALL when it is first defined.
        if full_name not in CITATION_REGISTRY_ALL:
            citation = CitationEntry.from_object(func, label=use_label)
            CITATION_REGISTRY_ALL[full_name] = citation
        else:
            logging.warning(f"Duplicated citation tag for function: {full_name}")

        # Wrap the function so it is marked as USED when it is called.
        if track_used:

            @wraps(func)
            def fun_wrapper(*args, **kwargs):
                # Save the citation as USED when it is first called.
                if func.__qualname__ not in CITATION_REGISTRY_USED:
                    CITATION_REGISTRY_USED.add(full_name)
                return func(*args, **kwargs)
        else:
            # We do not wrap the function, but just return the original function.
            fun_wrapper = func

            # We mark as used be default so the citation does not get dropped.
            CITATION_REGISTRY_USED.add(full_name)

        return fun_wrapper

    if callable(label):
        return decorator(label)
    return decorator


def cite_object(obj, label=None):
    """Add a citation for a specific object.

    Parameters
    ----------
    obj : object
        The object to add a citation for.
    label : str, optional
        The (optional) user-defined label for the citation.
    """
    full_name = _get_full_name(obj)
    if full_name not in CITATION_REGISTRY_ALL:
        CITATION_REGISTRY_ALL[full_name] = CitationEntry.from_object(obj, label=label)
    else:
        logging.warning(f"Duplicated citation tag for object: {full_name}")

    CITATION_REGISTRY_USED.add(full_name)


def get_all_citations():
    """Return a list of all citations in the software package.

    Returns
    -------
    citations : list of str
        A list of all citations in the software package.
    """
    citations = [str(entry) for entry in CITATION_REGISTRY_ALL.values()]
    return citations


def get_used_citations():
    """Return a list of all citations in the software package.

    Returns
    -------
    list of str
        A list of all citations in the software package.
    """
    citations = [str(CITATION_REGISTRY_ALL[func_name]) for func_name in CITATION_REGISTRY_USED]
    return citations


def find_in_citations(query, used_only=False):
    """Find a query string in the citation text. This is primarily used for
    testing, where a user might want to check if a citation is present.

    Parameters
    ----------
    query : str
        The query string to search for.
    used_only : bool, optional
        If True, only search in the used citations. If False, search in all citations.

    Returns
    -------
    matches : list of str
        A list of matching citation strings. This list is empty if no matches are found.
    """
    search_set = CITATION_REGISTRY_USED if used_only else CITATION_REGISTRY_ALL.keys()

    matches = []
    for name in search_set:
        entry = str(CITATION_REGISTRY_ALL[name])
        if query in entry:
            matches.append(entry)
    return matches


def reset_used_citations():
    """Reset the list of used citations."""
    CITATION_REGISTRY_USED.clear()


def print_all_citations():
    """Print all citations in the software package in a user-friendly way."""
    for name, citation in CITATION_REGISTRY_ALL.items():
        print(f"{name}:\n{citation.citation}\n")


def print_used_citations():
    """Print the used citations in the software package in a user-friendly way."""
    for name in CITATION_REGISTRY_USED:
        print(f"{name}:\n{CITATION_REGISTRY_ALL[name].citation}\n")
