from inspect import currentframe
from os import environ, makedirs, listdir, walk
from os.path import join, expanduser, isdir, isfile
from queue import Queue
from re import split, escape
from threading import Thread
from typing import Any

from .variables import aliaFolder


def cycle_list(list_: list | tuple):
    if len(list_) == 1: return list_
    return list_[1:] + list_[:1]


def human_readable_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


def get_files(root_: str = expanduser("~")) -> str:
    to_check_ = [root_]

    while to_check_:
        folder_ = to_check_.pop(0)

        try:
            contents_ = listdir(folder_)
        except PermissionError:
            continue

        for file_ in contents_:
            item = join(folder_, file_)

            if isdir(item):
                to_check_.append(item)
            elif isfile(item):
                yield item


def list_files_in_dir(root: str = "C:\\"):
    """AI GENERATED"""

    def worker_thread_(directory_, files_in_dir_, output_queue_):
        for file_name_ in files_in_dir_:
            file_path_ = join(directory_, file_name_)
            output_queue_.put(file_path_)

    file_queue_ = Queue()
    active_threads_ = []

    for current_directory_, subdirectories_, file_names_ in walk(root):
        thread_ = Thread(
            target=worker_thread_,
            args=(current_directory_, file_names_, file_queue_)
        )
        active_threads_.append(thread_)
        thread_.start()

    for thread_ in active_threads_:
        thread_.join()

    while not file_queue_.empty():
        yield file_queue_.get()


def default(current_var, default_value): return default_value if current_var is None else current_var


def gen_context(back: int = 1) -> dict[str, Any]:
    frame = currentframe()

    for _ in range(back):
        frame = frame.f_back

    return frame.f_locals


def re_split(input_string: str, delimiters: list[str]) -> list[str]:
    return split(f"[{''.join(map(escape, delimiters))}]", input_string)


def absorb(func):
    """Wrapper"""

    # noinspection PyUnusedLocal
    def do(*args, **kwargs):
        func()

    return do


class DefaultClass:
    def __repr__(
            self) -> str: return f"{type(self).__name__}({", ".join([f"{k}: {repr(v) if not callable(v) else v.__name__}" for k, v in self.__dict__.items()])})"


environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

makedirs(aliaFolder, exist_ok=True)

__all__ = ["aliaFolder", "cycle_list", "human_readable_size", "get_files", "list_files_in_dir", "default",
           "gen_context", "re_split", "absorb", "DefaultClass"]

if __name__ == '__main__':
    # DEBUGGING
    # TODO

    class Example:
        def __getitem__(self, args: slice):
            print(args.start, args.stop, args.step)


    test = Example()
    print(test["start":"stop":"step"])
