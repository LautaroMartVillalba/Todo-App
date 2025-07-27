import "./App.css";

function App() {
  function callPython() {
    (window as any).pywebview.api
      .get_all_tasks()
      .then((res, err) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });
  }
  return (
    <div className="text-2xl flex justify-center items-center h-[100vh]">
      <button onClick={callPython}>click me</button>
    </div>
  );
}

export default App;
