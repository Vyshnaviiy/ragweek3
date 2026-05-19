import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Analytics from "./pages/Analytics";
import Devices from "./pages/Devices";
import Billing from "./pages/Billing";
import NotFound from "./pages/NotFound";
import Sidebar from "./components/Sidebar";
import Chatbot from "./components/Chatbot";

function App() {

  return (

    <BrowserRouter>

      <div className="
        flex
        bg-gradient-to-br
        from-[#050816]
        to-[#0a0f1f]
        text-white
        min-h-screen
      ">

        <Sidebar />

        <div className="
          flex-1
          overflow-auto
        ">

          <Routes>

            <Route
              path="/"
              element={<Navigate to="/dashboard" />}
            />

            <Route
              path="/dashboard"
              element={<Dashboard />}
            />

            <Route
              path="/analytics"
              element={<Analytics />}
            />

            <Route
              path="/devices"
              element={<Devices />}
            />

            <Route
              path="/billing"
              element={<Billing />}
            />

            <Route
              path="*"
              element={<NotFound />}
            />

          </Routes>

        </div>

        <Chatbot />

      </div>

    </BrowserRouter>
  );
}

export default App;