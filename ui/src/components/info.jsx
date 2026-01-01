// InfoDialog.jsx
import { X, Info } from "lucide-react";

const InfoDialog = ({ open, closeFn }) => {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-100 flex items-center justify-center bg-black/40 backdrop-blur-sm">
      <div className="w-full max-w-xl rounded-xl bg-white p-6 shadow-xl relative">
        <button
          onClick={() => closeFn(false)}
          className="absolute right-4 top-4 text-black font-bold cursor-pointer"
        >
          <X size={24} />
        </button>

        <div className="flex items-center gap-2 mb-3">
          <Info size={18} className="text-blue-600" />
          <h2 className="text-lg font-semibold text-gray-800">
            JSON File Format
          </h2>
        </div>

        <p className="text-md text-gray-600 leading-relaxed">
          • This file should have an mandotary field of time_of_day, session_length, Noise_State(measured in decibels). 
        </p>
        
        <p className="text-md text-gray-600 leading-relaxed">
          • This file should consists of the absolute values of all signals. In case some signals are missing which could be due to unability to measure them then that signal can be ommitted.
        </p>
        
      </div>
    </div>
  );
};

export default InfoDialog;
