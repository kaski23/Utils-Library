# parallel_utils.py
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from typing import Callable, Iterable, Any, List, Literal
import os


def _call_func(func: Callable, item: Any):
    """Hilfsfunktion: erkennt Tuple/List und entpackt automatisch."""
    if isinstance(item, (tuple, list)):
        return func(*item)
    else:
        return func(item)


def run_parallel_list(
    func: Callable[..., Any],
    data: Iterable[Any],
    workers: int = None,
    backend: Literal["thread", "process"] = "process",
    progress: bool = False
) -> List[Any]:
    """
    Parallele Ausführung für materialisierte Daten (Liste, Range, Array ...).
    Ergebnisse werden in Eingabereihenfolge zurückgegeben.
    """
    if workers is None:
        workers = os.cpu_count() or 1

    Executor = ThreadPoolExecutor if backend == "thread" else ProcessPoolExecutor
    data = list(enumerate(data))  # materialisieren + Index
    results = [None] * len(data)

    if progress:
        try:
            from tqdm import tqdm
            iterator = tqdm(data, desc="Parallel (list)", unit="task")
        except ImportError:
            iterator = data
    else:
        iterator = data

    with Executor(max_workers=workers) as executor:
        future_to_index = {
            executor.submit(_call_func, func, item): idx
            for idx, item in iterator
        }
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            results[idx] = future.result()

    return results


def run_parallel_stream(
    func: Callable[..., Any],
    data: Iterable[Any],
    workers: int = None,
    backend: Literal["thread", "process"] = "process",
    progress: bool = False
) -> Iterable[Any]:
    """
    Parallele Ausführung für Lazy-Iterables (Generatoren, Streams).
    Ergebnisse werden **ungeordnet** geliefert (sobald fertig).
    Gibt einen Generator zurück.
    """
    if workers is None:
        workers = os.cpu_count() or 1

    Executor = ThreadPoolExecutor if backend == "thread" else ProcessPoolExecutor

    if progress:
        try:
            from tqdm import tqdm
            iterator = tqdm(data, desc="Parallel (stream)", unit="task")
        except ImportError:
            iterator = data
    else:
        iterator = data

    def generator():
        with Executor(max_workers=workers) as executor:
            futures = {executor.submit(_call_func, func, item) for item in iterator}
            for future in as_completed(futures):
                yield future.result()

    return generator()
