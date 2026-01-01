import { useState , useRef} from "react";
import {
  Upload,
  AlertCircle,
  CheckCircle,
  Activity,
  Info
} from "lucide-react";
import Navbar from "../components/navbar.jsx";
import InfoDialog from "../components/info.jsx";

/* ---------- OPTIONS (KEYS ONLY) ---------- */

const ACCESS_LEVEL = {
  PI: "Physical Intervention by Attacker needed to exploit",
  SS: "Access to the Shell or the System of the worker needed to exploit",
  SN: "Need to enter a Secured LAN/WiFi network in which scenario exists",
  PN: "Scenario exists in a Public Network which is easier to enter ",
  OS: "The resources are Open sourced for exploitation"
};

const ATTACKING_SKILL = {
  EASY: "Technical Low attackigng skill like Phishing, Spam, Exposed Credentials exploitation needed",
  INTERMEDIATE: "Exploitation needs technical understandig of the systems/softwares, as in case of Unpatched softwares or basic SQL injection",
  COMPLEX: "Complicated steps needed for exploitation, which includes expensive computational setup, interaction with firmwares etc."
};

const USER_INTERACTION = {
  NO: "The system operates automatically and needs no human intervention/directions for actions to be performed.",
  YES: "The attack needs intervention of a third person action(like Accept or Link Click) to to be successfull"
};

const COMPANY_RESOURCES = {
  NONE: "Almost no real resources or assets(could be monetary or other) is directly or indirectly associated with the system",
  LOW: "Very minimal assets at stake which sum up to less than 1% of the company value",
  MID: "Assest of near about 5% or slight less is directly or indirectly associated with the system which could be at risk on exploitation",
  HIGH: "More than 5% of companies value is directly or indirectly associated with the system's exploitation"
};

const ENVIRONMENT = {
  SOL: "The Work is being done in complete Solitude",
  SMG: "Work is being done by a Small group of people who can be organized conviniently",
  OFE: "Person is working in an Office environment with like-minded peers",
  HSE: "Highly stimulus Environment is present around the person working"
};

/* ---------- SMALL UI HELPERS ---------- */

const RadioGroup = ({ title, options, value, onChange }) => (
  <div className="space-y-2 mb-8">
    <h3 className="text-md font-bold text-blue-500">{title}</h3>

    <div className="space-y-1">
      {Object.entries(options).map(([key, desc]) => {
        const selected = value === key;

        return (
          <label
            key={key}
            className={`flex items-start gap-2 cursor-pointer rounded-md p-2 border-l-4 transition
              ${
                selected
                  ? "border-l-blue-500 bg-blue-50"
                  : "border-l-transparent hover:bg-gray-100"
              }`}
          >
            <input
              type="radio"
              checked={selected}
              onChange={() => onChange(key)}
              className="mt-1"
            />
            <div>
              {/* <p className="text-md font-medium">{key}</p> */}
              <p className="text-sm text-black font-medium">{desc}</p>
            </div>
          </label>
        );
      })}
    </div>
  </div>
);


/* ---------- CHARTS (PURE SVG) ---------- */
const PieChart = ({ data }) => {
  const entries = Object.entries(data)
    .sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
    .slice(0, 7);
  const total = entries.reduce((a, [, v]) => a + Math.abs(v), 0);

  let acc = 0;
  const colors = [
    "#3b82f6",
    "#22c55e",
    "#f97316",
    "#a855f7",
    "#ef4444",
    "#06b6d4",
    "#84cc16"
  ];

  return (
    <div className="flex flex-col md:flex-row gap-4 chart-animate justify-around">
      {/* PIE */}
      <svg viewBox="0 0 200 200" className="w-full md:w-64 h-64">
        {entries.map(([key, value], i) => {
          const start = acc / total;
          const slice = Math.abs(value) / total;
          acc += Math.abs(value);

          const x1 = 100 + 100 * Math.cos(2 * Math.PI * start);
          const y1 = 100 + 100 * Math.sin(2 * Math.PI * start);
          const x2 = 100 + 100 * Math.cos(2 * Math.PI * (start + slice));
          const y2 = 100 + 100 * Math.sin(2 * Math.PI * (start + slice));
          const large = slice > 0.5 ? 1 : 0;

          return (
            <path
              key={key}
              d={`M100 100 L${x1} ${y1} A100 100 0 ${large} 1 ${x2} ${y2} Z`}
              fill={colors[i % colors.length]}
            >
              <title>{`${key}: ${value.toFixed(3)}`}</title>
            </path>
          );
        })}
      </svg>

      {/* LEGEND */}
      <div className="flex flex-col space-y-2 text-md">
        {entries.map(([key, value], i) => (
          <div key={key} className="flex items-center gap-2">
            <span
              className="w-3 h-3 rounded-sm"
              style={{ backgroundColor: colors[i % colors.length] }}
            />
            <span className="flex-1 truncate">{key}</span>
            <span className="text-gray-500">
              {value.toFixed(2)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

const HistogramChart = ({ data }) => {
  const top10 = Object.entries(data)
    .sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))
    .slice(0, 10);

  const max = Math.max(...top10.map(([, v]) => Math.abs(v)));

  return (
    <div className="chart-animate">
      <div className="flex flex-col gap-4">
        {top10.map(([key, value]) => {
          const width = (Math.abs(value) / max) * 100;

          return (
            <div key={key} className="flex items-center gap-4 group relative">
              {/* LABEL */}
              <div className="w-40 text-sm text-gray-600 font-semibold text-right">
                {key
                  .replaceAll("_", "  _")
                  .split("_")
                  .filter(
                    (word) =>
                      !(
                        word.toLowerCase() === "ms" ||
                        word.toLowerCase() === "in"
                      )
                  )}
              </div>

              {/* BAR CONTAINER */}
              <div className="flex-1 h-6 bg-gray-200 rounded flex items-center relative">
                <div
                  className="h-6 bg-blue-500 rounded-r transition-all duration-700 group-hover:bg-blue-600"
                  style={{ width: `${width}%` }}
                />

                {/* TOOLTIP */}
                <div className="absolute left-2 -top-10 opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none">
                  <div className="bg-gray-300 text-black text-sm font-medium px-3 py-1.5 rounded-md shadow-lg whitespace-nowrap">
                    {key.replaceAll("_", " ")} : {value.toFixed(3)}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <p className="mt-3 text-md text-gray-500 text-center">
        Top 10 signals by absolute contribution
      </p>
    </div>
  );
};




/* ---------- MAIN COMPONENT ---------- */

export default function Dashboard() {
  const [signals, setSignals] = useState(null);
  const [accessLevel, setAccessLevel] = useState("");
  const [attackingSkill, setAttackingSkill] = useState("");
  const [userInteraction, setUserInteraction] = useState("");
  const [companyResources, setCompanyResources] = useState("");
  const [environment, setEnvironment] = useState("");
  const [companyPublic, setCompanyPublic] = useState(false);
  const [timeOfDay, setTimeOfDay] = useState("");
  const [sessionLength, setSessionLength] = useState(0);
  const [noise, setNoise] = useState(0);

  const [response, setResponse] = useState(null);
  const [error, setError] = useState("");

  const [fileName, setFileName] = useState("");
  const [fileValid, setFileValid] = useState(false);
  const fileInputRef = useRef(null);

  const [openInfo ,  setOpenInfo] = useState(false)

  

  /* ---------- JSON UPLOAD ---------- */

const handleFile = (e) => {
  const file = e.target.files[0];

  if (!file) return;

  if (file.type !== "application/json") {
    setError("Only JSON files are allowed");
    setFileValid(false);
    setFileName("");
    return;
  }

  const reader = new FileReader();

  reader.onload = () => {
    try {
      const parsed = JSON.parse(reader.result);

      // extract required fields
      const {
        time_of_day,
        session_length,
        Noise_State,
        ...signalsOnly
      } = parsed;

      setTimeOfDay(time_of_day);
      setSessionLength(session_length);
      setNoise(noise);

      setSignals(signalsOnly);
      setFileName(file.name);
      setFileValid(true);
      setError("");
    } catch {
      setError("Invalid JSON structure");
      setFileValid(false);
      setFileName("");
    }
  };


  reader.readAsText(file);
};

const removeFile = () => {
  setSignals(null);
  setFileName("");
  setFileValid(false);
  setError("");
  if (fileInputRef.current) {
    fileInputRef.current.value = "";
  }
};



  /* ---------- API CALL ---------- */

  const submit = async () => {
    try {
      setError("");

      const body = {
        signals,
        time_of_day: timeOfDay,
        session_length: sessionLength,
        noise,
        environmental_factor: environment,
        access_level: accessLevel,
        attacking_skill: attackingSkill,
        user_interaction: userInteraction,
        company_resources_stake: companyResources,
        company_resources_public: companyPublic
      };


      const res = await fetch(`${import.meta.env.VITE_API_URL}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });

      if (!res.ok) throw new Error("API request failed");
      setResponse(await res.json());
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen mt-20 bg-gray-50 flex flex-col overflow-hidden">
      <Navbar />
      <InfoDialog open={openInfo} closeFn={setOpenInfo}/>
      
      <div className="min-h-screen bg-gray-50 flex flex-col lg:flex-row overflow-hidden">
        
        {/* ---------- LEFT PANEL ---------- */}
        <div className="lg:w-[30%] bg-white p-6 space-y-6 overflow-y-auto max-h-screen cursor-pointer">
        
          <h2 className="text-xl font-bold flex items-center gap-2">
            <Activity size={18} /> Input Parameters
          </h2>

          <div className="relative">
            <button
              onClick={() => setOpenInfo(true)}
              className="cursor-pointer absolute -top-8 -right-3 w-7 h-7 rounded-full bg-blue-500 text-white flex items-center justify-center shadow hover:bg-blue-600 transition"
            >
              <Info size={20} />
            </button>
            <div
              className={`flex items-center justify-between gap-3 p-3 border rounded transition
                ${fileValid ? "border-green-500 bg-green-50" : "hover:bg-gray-100"}
              `}
            >
              <label className="flex items-center gap-2 cursor-pointer">
                {fileValid ? (
                  <CheckCircle size={16} className="text-green-600" />
                ) : (
                  <Upload size={16} />
                )}

                <div className="flex flex-col">
                  <span className="text-md font-medium">
                    {fileValid ? "JSON Uploaded" : "Upload Signals JSON"}
                  </span>

                  {fileName && (
                    <span className="text-md text-gray-500 truncate max-w-[160px]">
                      {fileName}
                    </span>
                  )}
                </div>

                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".json"
                  hidden
                  onChange={handleFile}
                />
              </label>

              {fileValid && (
                <button
                  onClick={removeFile}
                  className="text-xs font-medium text-red-600 hover:underline cursor-pointer"
                >
                  Remove
                </button>
              )}
            </div>
          </div>


          <RadioGroup title="Access Level(AL)" options={ACCESS_LEVEL} value={accessLevel} onChange={setAccessLevel} />
          <RadioGroup title="Attacking Skill(AS)" options={ATTACKING_SKILL} value={attackingSkill} onChange={setAttackingSkill} />
          <RadioGroup title="User Interaction(UI)" options={USER_INTERACTION} value={userInteraction} onChange={setUserInteraction} />
          <RadioGroup title="Company Resources Stake(CTC)" options={COMPANY_RESOURCES} value={companyResources} onChange={setCompanyResources} />
          <RadioGroup title="Environmental Factor(ENV)" options={ENVIRONMENT} value={environment} onChange={setEnvironment} />

          {/* Toggle */}
          <div>
            <h3 className="text-md font-semibold">Company Resources Public</h3>
            <p className="text-md text-gray-500 mb-2">
              Indicates if information about resources associated with are publicly accessible
            </p>
            <button
              onClick={() => setCompanyPublic(!companyPublic)}
              className={`w-12 h-6 rounded-full relative transition ${
                companyPublic ? "bg-blue-500" : "bg-gray-300"
              }`}
            >
              <span
                className={`absolute top-1 w-4 h-4 bg-white rounded-full transition ${
                  companyPublic ? "left-7" : "left-1"
                }`}
              />
            </button>
          </div>

          <button
            onClick={submit}
            className="w-full bg-blue-600 text-xl text-white py-4 font-semibold rounded-lg hover:bg-blue-700 cursor-pointer"
          >
            Calculate Score
          </button>

          {error && (
            <p className="text-sm text-red-600 flex gap-1">
              <AlertCircle size={14} /> {error}
            </p>
          )}
        
        </div>

        {/* ---------- RIGHT PANEL ---------- */}
        <div className="lg:w-[70%] p-6 space-y-6 overflow-y-auto max-h-screen">

          {!response && (
            <div className="h-full flex items-center justify-center text-gray-400">
              Submit inputs to view dashboard
            </div>
          )}

          {response && (
            <>
              {/* Summary */}
              <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
                {[
                  ["Total Score", response.total_score.toFixed(3)],
                  ["Base Score", response.base_score.toFixed(3)],
                  ["Multiplier", response.multiplier.toFixed(3)],
                  ["Exploit Modifier" , response.exploit_modifier.toFixed(3)],
                  ["Exploit Band", response.exploit_band]
                ].map(([label, val]) => (
                  <div key={label} className="bg-white p-4 rounded shadow-sm">
                    <p className="text-md font-semibold text-gray-500">{label}</p>
                    <p className="text-lg font-bold">{val}</p>
                  </div>
                ))}
              </div>

              {/* Charts */}
              <div className="flex flex-col gap-6">
                <div className="bg-white p-4 rounded shadow-sm">
                  <h3 className="text-xl font-semibold mb-2">State Weights</h3>
                  <PieChart data={response.state_weights} />
                </div>

                <div className="bg-white p-4 rounded shadow-sm">
                  <h3 className="text-xl font-semibold mb-2">Signal Weights</h3>
                  <HistogramChart data={response.signal_weights} />
                </div>
              </div>
            </>
          )}
        </div>
      </div>

    </div>
  );
}
