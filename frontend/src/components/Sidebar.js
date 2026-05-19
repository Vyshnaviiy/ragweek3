import {
  LayoutDashboard,
  BarChart3,
  PlugZap,
  Wallet
} from "lucide-react";

import { NavLink } from "react-router-dom";
import { motion } from "framer-motion";

function Sidebar() {

  const linkClass = ({ isActive }) =>
    `flex items-center gap-3 px-5 py-4 rounded-2xl transition-all duration-300 relative overflow-hidden
    ${isActive
      ? "bg-gradient-to-r from-blue-600/20 to-cyan-500/20 text-white shadow-lg border border-blue-500/30"
      : "text-gray-400 hover:bg-[#111827] hover:text-white hover:border hover:border-gray-700"
    }`;

  return (
    <motion.div
      initial={{ x: -100, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="
        w-72
        bg-[#0B1120]/80
        backdrop-blur-xl
        border-r
        border-gray-800/50
        p-6
        flex
        flex-col
        justify-between
        shadow-2xl
      "
    >
      <div>
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="
            text-4xl
            font-black
            mb-12
            bg-gradient-to-r
            from-orange-400
            via-red-500
            to-pink-500
            text-transparent
            bg-clip-text
            drop-shadow-lg
          "
        >
          ⚡ VoltStream
        </motion.h1>

        <div className="space-y-3">
          <NavLink
            to="/dashboard"
            className={linkClass}
          >
            {({ isActive }) => (
              <>
                {isActive && (
                  <motion.div
                    layoutId="activeGlow"
                    className="absolute inset-0 bg-gradient-to-r from-blue-600/30 to-cyan-500/30 rounded-2xl blur-sm"
                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                  />
                )}
                <LayoutDashboard size={22} />
                <span className="relative z-10">Live Dashboard</span>
              </>
            )}
          </NavLink>

          <NavLink
            to="/analytics"
            className={linkClass}
          >
            {({ isActive }) => (
              <>
                {isActive && (
                  <motion.div
                    layoutId="activeGlow"
                    className="absolute inset-0 bg-gradient-to-r from-blue-600/30 to-cyan-500/30 rounded-2xl blur-sm"
                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                  />
                )}
                <BarChart3 size={22} />
                <span className="relative z-10">Usage History</span>
              </>
            )}
          </NavLink>

          <NavLink
            to="/devices"
            className={linkClass}
          >
            {({ isActive }) => (
              <>
                {isActive && (
                  <motion.div
                    layoutId="activeGlow"
                    className="absolute inset-0 bg-gradient-to-r from-blue-600/30 to-cyan-500/30 rounded-2xl blur-sm"
                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                  />
                )}
                <PlugZap size={22} />
                <span className="relative z-10">Smart Control</span>
              </>
            )}
          </NavLink>

          <NavLink
            to="/billing"
            className={linkClass}
          >
            {({ isActive }) => (
              <>
                {isActive && (
                  <motion.div
                    layoutId="activeGlow"
                    className="absolute inset-0 bg-gradient-to-r from-blue-600/30 to-cyan-500/30 rounded-2xl blur-sm"
                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                  />
                )}
                <Wallet size={22} />
                <span className="relative z-10">Billing</span>
              </>
            )}
          </NavLink>
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.5 }}
        className="
          bg-[#111827]/50
          backdrop-blur-sm
          border
          border-gray-800/50
          rounded-2xl
          p-5
          shadow-lg
        "
      >
        <p className="text-sm text-gray-400">
          Tachyon AIML Intern
        </p>
        <h2 className="mt-2 font-bold text-cyan-400">
          Prosumer Copilot v4.0
        </h2>
      </motion.div>
    </motion.div>
  );
}

export default Sidebar;