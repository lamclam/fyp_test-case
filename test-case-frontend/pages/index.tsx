import { useState, Fragment } from "react";
import axios from "axios";
import { DotLoader } from "react-spinners";
import { Dialog, Transition } from "@headlessui/react";

export default function Home() {
  const [javaCode, setJavaCode] = useState("");
  const [javaCodeResult, setJavaCodeResult] = useState<any[]>([]);
  const [passCount, setPassCount] = useState(0);
  const [failCount, setFailCount] = useState(0);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [prediction, setPrediction] = useState("");
  const [showErrorList, setShowErrorList] = useState(false);

  const handleReset = (btn = false) => {
    if (btn) {
      setJavaCodeResult([]);
      setPassCount(0);
      setFailCount(0);
      setTotalCount(0);
      setErrorMessage("");
      setPrediction("");
      setShowErrorList(false);
      setJavaCode("");
    } else {
      setJavaCodeResult([]);
      setPassCount(0);
      setFailCount(0);
      setTotalCount(0);
      setErrorMessage("");
      setPrediction("");
      setShowErrorList(false);
    }
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      handleReset();

      const options = {
        method: "POST",
        url: "http://127.0.0.1:5000/run_code",
        headers: { "content-type": "text/plain" },
        data: javaCode,
      };
      const response = await axios.request(options);
      console.log(response.data);
      if (response.status !== 200) {
        console.error("Invalid response status", response);
        return;
      }

      const data = response.data;
      if (!data) {
        console.error("Empty response");
        return;
      }

      if (data.error) {
        setErrorMessage(data.error);
        return;
      }

      console.log(data.prediction);
      if (data.prediction && data.prediction >= 0)
        setPrediction(data.prediction);
      const results = data.results;
      if (Array.isArray(results)) {
        const outputData = results.map((result) => {
          const { stdin, stdout, pass, expected } = result;
          return {
            stdin: stdin,
            stdout: stdout,
            pass: pass,
            expected: expected,
          };
        });
        console.log(outputData);
        setJavaCodeResult(outputData);

        const totalCount = outputData.length;
        const passCount = outputData.filter(
          (result) => result.pass === true
        ).length;
        const failCount = outputData.reduce((count, result) => {
          if (result.pass === false || result.pass === "Error") {
            return count + 1;
          }
          return count;
        }, 0);
        setPassCount(passCount);
        setFailCount(failCount);
        setTotalCount(totalCount);
      } else {
        console.error("Invalid response format");
        console.error(results);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col justify-center items-center">
      <Transition appear show={loading} as={Fragment}>
        <Dialog as="div" className="relative z-10" onClose={() => {}}>
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
          </Transition.Child>

          <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
            <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
              <Transition.Child
                as={Fragment}
                enter="ease-out duration-300"
                enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
                enterTo="opacity-100 translate-y-0 sm:scale-100"
                leave="ease-in duration-200"
                leaveFrom="opacity-100 translate-y-0 sm:scale-100"
                leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              >
                <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-sm sm:p-6">
                  <Dialog.Title
                    as="h3"
                    className="text-2xl font-bold leading-6 text-gray-900 flex justify-center items-center flex-row gap-x-8"
                  >
                    <DotLoader color="#36d7b7" />
                    Loading
                  </Dialog.Title>
                </Dialog.Panel>
              </Transition.Child>
            </div>
          </div>
        </Dialog>
      </Transition>
      <div className="mx-auto w-11/12 px-4 h-5/6 py-8 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 h-full md:grid-cols-2 md:gap-4">
          <div className="mx-auto w-full px-4 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-3xl h-full">
              <div className="flex flex-col justify-center items-center h-full">
                <div className="flex flex-col w-full h-full">
                  <label
                    htmlFor="javaCode"
                    className="block font-medium leading-6 text-gray-100 text-2xl pb-4"
                  >
                    Enter your Java code here
                  </label>
                  <div className="mt-2 grow">
                    <textarea
                      name="javaCode"
                      id="javaCode"
                      value={javaCode}
                      onChange={(e) => setJavaCode(e.target.value)}
                      className="block w-full rounded-md border-0 py-1.5 text-gray-100 bg-black shadow-sm ring-1 ring-inset ring-gray-300 h-full placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                    />
                  </div>
                  <div className="mt-2 flex justify-end gap-x-2">
                    <button
                      type="button"
                      onClick={() => handleReset(true)}
                      className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-sky-600 hover:bg-sky-500 focus:outline-none"
                    >
                      Reset
                    </button>
                    <button
                      type="button"
                      onClick={handleSubmit}
                      className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-500 focus:outline-none"
                    >
                      Submit
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="mx-auto w-full max-w-7xl px-4 max-h-full overflow-y-scroll sm:px-6 lg:px-8">
            <div className="mx-auto max-w-4xl max-h-full">
              {/* wrong result list */}
              {failCount > 0 && (
                <div className="flex flex-col justify-center items-center">
                  <div className="flex flex-row pb-4 w-full h-full">
                    <p className="text-gray-100 text-2xl sticky top-0 bg-black">
                      Oops! Your code failed some test cases
                    </p>
                    <button
                      className="ml-4 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-teal-600 hover:bg-teal-500 focus:outline-none"
                      onClick={() => setShowErrorList(!showErrorList)}
                    >
                      Show/Hide Errors
                    </button>
                  </div>
                  {showErrorList && (
                    <div className="space-y-4 max-h-full w-full">
                      {javaCodeResult.map((result) => {
                        if (result.pass === false || result.pass === "Error") {
                          return (
                            <div
                              key={`${result.stdin}-${result.stdout}`}
                              className={`card fail grid grid-cols-5 gap-y-4`}
                            >
                              <h3 className="font-bold col-span-1">
                                Test Case
                              </h3>
                              <p className="col-span-4">{result.stdin}</p>
                              <h3 className="font-bold col-span-1">Status</h3>
                              <p className="col-span-4">
                                {String(result.pass).charAt(0).toUpperCase() +
                                  String(result.pass).slice(1)}
                              </p>
                              <h3 className="font-bold col-span-1">Output</h3>
                              <p className="col-span-4">{result.stdout}</p>
                            </div>
                          );
                        }
                        return null; // Skip rendering for other cases
                      })}
                    </div>
                  )}
                  {/* total count */}
                  <div className="text-white pt-4 sticky bottom-0 bg-black grid grid-cols-12 gap-2 w-full">
                    <h3 className="font-bold col-span-2 justify-self-end">
                      Total Count:
                    </h3>
                    <h3 className="font-bold col-span-10">{totalCount}</h3>
                    <h3 className="font-bold col-span-2 justify-self-end">
                      Pass Count:
                    </h3>
                    <h3 className="font-bold col-span-10">{passCount}</h3>
                    <h3 className="font-bold col-span-2 justify-self-end">
                      Fail Count:
                    </h3>
                    <h3 className="font-bold col-span-10">{failCount}</h3>
                    <h3 className="font-bold col-span-2 justify-self-end">
                      Prediction:
                    </h3>
                    <h3 className="font-bold col-span-10">{prediction}</h3>
                  </div>
                  {/* Suggestion */}
                  <div className="flex flex-row py-8 w-full h-full">
                    <p className="text-gray-100 text-2xl sticky top-0 bg-black">
                      Suggestion
                    </p>
                  </div>
                </div>
              )}
              {passCount > 0 && failCount === 0 && (
                <div className="flex flex-col justify-center items-center">
                  <div className="flex flex-row pb-4 w-full h-full">
                    <p className="text-gray-100 text-2xl sticky top-0 bg-black">
                      Congratulations! Your code passed all test cases
                    </p>
                  </div>
                  {/* total count */}
                  <div className="text-white pt-4 sticky bottom-0 bg-black grid grid-cols-12 gap-2 w-full">
                    <h3 className="font-bold col-span-2 justify-self-end">
                      Total Count:
                    </h3>
                    <h3 className="font-bold col-span-10">{totalCount}</h3>
                    <h3 className="font-bold col-span-2 justify-self-end">
                      Pass Count:
                    </h3>
                    <h3 className="font-bold col-span-10">{passCount}</h3>
                    <h3 className="font-bold col-span-2 justify-self-end">
                      Fail Count:
                    </h3>
                    <h3 className="font-bold col-span-10">{failCount}</h3>
                    <h3 className="font-bold col-span-2 justify-self-end">
                      Prediction:
                    </h3>
                    <h3 className="font-bold col-span-10">{prediction}</h3>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
