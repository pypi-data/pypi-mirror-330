# -- import packages: ---------------------------------------------------------
import ABCParse
import concurrent.futures
import os
import time


# -- operational class: -------------------------------------------------------
class ParallelExecutor(ABCParse.ABCParse):
    def __init__(self, max_threads: int = 8, *args, **kwargs) -> None:
        self.__parse__(locals())

        self._RESULTS = {}

    def _forward(self, future_jobs, future) -> None:
        k, v = future_jobs[future]
        try:
            self._RESULTS[k] = future.result()
        except Exception as e:
            print(f"Error for id: {k}: {str(e)}\n")

    def forward(self, function, input):
        self._start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self._max_threads
        ) as executor:
            future_jobs = {
                executor.submit(function, **v if isinstance(v, dict) else {'value': v}): [k, v] 
                for k, v in input.items()
            }
            for future in concurrent.futures.as_completed(future_jobs):
                self._forward(future_jobs, future)
        self._end_time = time.time()
        return future_jobs

    @property
    def _total_time(self):
        return self._end_time - self._start_time

    def __call__(self, function, input) -> dict:
        """
        Execute the given function in parallel, up to the number of threads specified.

        Args:
            function (callable): The function to execute.
            input (dict): The input to the function.

        Returns:
            dict: The results of the function.
        """
        self.future_jobs = self.forward(function, input)
        print(f"Total time taken: {self._total_time:.2f} seconds")
        return self._RESULTS

# -- function: ----------------------------------------------------------------
def parallel_execution(
    function: callable,
    input: dict,
    max_threads: int = os.cpu_count()*0.8,
) -> dict:
    """
    Execute the given function in parallel, up to the number of threads specified.
    """
    executor = ParallelExecutor(max_threads=max_threads)
    return executor(function, input)
