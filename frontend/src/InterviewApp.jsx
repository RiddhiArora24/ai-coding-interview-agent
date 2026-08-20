import {
  useEffect,
  useMemo,
  useState
} from "react";

import Editor from "@monaco-editor/react";

import {
  ArrowLeft,
  ArrowRight,
  BarChart3,
  Brain,
  BriefcaseBusiness,
  Check,
  CheckCircle2,
  ChevronRight,
  Clock3,
  Code2,
  Flame,
  Gauge,
  Lightbulb,
  LoaderCircle,
  Play,
  RotateCcw,
  Send,
  ShieldCheck,
  Sparkles,
  Terminal,
  Trophy,
  UserRound,
  X,
  XCircle
} from "lucide-react";

import {
  finishInterview,
  getCompanies,
  getHint,
  getQuestion,
  getSolution,
  runCode,
  startInterview,
  submitCode
} from "./api";


const COMPANY_INFO = {

  "Amazon": {
    icon: "A",
    description:
      "Arrays, hashing, graphs and scalable problem solving",
    accent: "amazon"
  },

  "Google": {
    icon: "G",
    description:
      "Algorithms, DP, graphs and analytical problem solving",
    accent: "google"
  },

  "Microsoft": {
    icon: "M",
    description:
      "Core DSA, dynamic programming and implementation",
    accent: "microsoft"
  },

  "Meta": {
    icon: "M",
    description:
      "Fast problem solving, arrays, strings and graphs",
    accent: "meta"
  },

  "Goldman Sachs": {
    icon: "GS",
    description:
      "Algorithms, arrays, greedy and quantitative thinking",
    accent: "goldman"
  }
};


const DIFFICULTIES = [

  {
    name: "Easy",
    description:
      "Fundamentals, clean implementation and core data structures",
    icon: Gauge
  },

  {
    name: "Medium",
    description:
      "Standard technical interview difficulty",
    icon: Flame
  },

  {
    name: "Hard",
    description:
      "Advanced algorithms and optimization",
    icon: Brain
  }
];


function formatTime(seconds) {

  const safe = Math.max(
    0,
    Number(seconds || 0)
  );

  const minutes = Math.floor(
    safe / 60
  );

  const secs = safe % 60;

  return `${String(minutes).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
}


function LoadingScreen({
  text = "Loading..."
}) {

  return (
    <div className="page-center">

      <div className="loading-card">

        <LoaderCircle
          size={34}
          className="spin"
        />

        <div>
          {text}
        </div>

      </div>

    </div>
  );
}


function ErrorBanner({
  message,
  onClose
}) {

  if (!message) {
    return null;
  }

  return (
    <div className="error-banner">

      <XCircle size={19} />

      <span>
        {message}
      </span>

      <button
        onClick={onClose}
        type="button"
      >
        <X size={17} />
      </button>

    </div>
  );
}


function App() {

  const [profile, setProfile] =
    useState(null);

  const [authError, setAuthError] =
    useState("");

  const [companies, setCompanies] =
    useState([]);

  const [screen, setScreen] =
    useState("dashboard");

  const [company, setCompany] =
    useState("");

  const [difficulty, setDifficulty] =
    useState("");

  const [sessionId, setSessionId] =
    useState("");

  const [position, setPosition] =
    useState(1);

  const [question, setQuestion] =
    useState(null);

  const [language, setLanguage] =
    useState("python");

  const [codes, setCodes] =
    useState({});

  const [submitted, setSubmitted] =
    useState({});

  const [remaining, setRemaining] =
    useState(3600);

  const [runResult, setRunResult] =
    useState(null);

  const [submitResult, setSubmitResult] =
    useState(null);

  const [hint, setHint] =
    useState("");

  const [report, setReport] =
    useState(null);

  const [solutions, setSolutions] =
    useState([]);

  const [busy, setBusy] =
    useState(false);

  const [actionBusy, setActionBusy] =
    useState("");

  const [error, setError] =
    useState("");


  // ==========================================================
  // LOCAL APPLICATION PROFILE
  // AI Pipe API key is stored securely in backend .env
  // ==========================================================

  useEffect(() => {

    try {

      const saved =
        localStorage.getItem(
          "auth_user"
        );

      if (saved) {

        setProfile(
          JSON.parse(saved)
        );

      } else {

        setProfile({
          name: "Candidate",
          email: "Candidate"
        });

      }

    } catch {

      setProfile({
        name: "Candidate",
        email: "Candidate"
      });

    }

  }, []);


  // ==========================================================
  // LOAD COMPANIES
  // ==========================================================

  useEffect(() => {

    if (!profile) {
      return;
    }

    async function load() {

      try {

        const data =
          await getCompanies();

        setCompanies(
          data.companies || []
        );
      }
      catch (err) {

        setError(
          err.message
        );
      }
    }

    load();

  }, [profile]);


  // ==========================================================
  // TIMER
  // ==========================================================

  useEffect(() => {

    if (
      screen !== "interview"
    ) {
      return;
    }

    const timer =
      setInterval(() => {

        setRemaining(
          current =>
            Math.max(
              0,
              current - 1
            )
        );

      }, 1000);

    return () =>
      clearInterval(timer);

  }, [screen]);


  // ==========================================================
  // CURRENT CODE
  // ==========================================================

  const codeKey =
    `${position}-${language}`;

  const currentCode =
    codes[codeKey] || "";


  const submittedCount =
    Object.values(
      submitted
    ).filter(Boolean).length;


  const allSubmitted =
    submittedCount >= 4;


  // ==========================================================
  // START INTERVIEW
  // ==========================================================

  async function beginInterview() {

    if (
      !company ||
      !difficulty
    ) {
      return;
    }

    setBusy(true);
    setError("");

    try {

      const data =
        await startInterview(
          company,
          difficulty
        );

      setSessionId(
        data.session_id
      );

      setRemaining(
        data.duration_seconds
      );

      setSubmitted({});
      setCodes({});
      setPosition(1);

      await loadQuestion(
        data.session_id,
        1
      );

      setScreen(
        "interview"
      );
    }
    catch (err) {

      setError(
        err.message
      );
    }
    finally {

      setBusy(false);
    }
  }


  // ==========================================================
  // LOAD QUESTION
  // ==========================================================

  async function loadQuestion(
    sid,
    nextPosition
  ) {

    setActionBusy(
      "question"
    );

    setError("");

    try {

      const data =
        await getQuestion(
          sid,
          nextPosition
        );

      setQuestion(data);

      setPosition(
        nextPosition
      );

      setRemaining(
        data.remaining_seconds
      );

      setRunResult(null);
      setSubmitResult(null);
      setHint("");

      if (
        data.already_submitted
      ) {

        setSubmitted(
          previous => ({
            ...previous,
            [nextPosition]: true
          })
        );
      }

      setCodes(
        previous => {

          const next = {
            ...previous
          };

          const pythonKey =
            `${nextPosition}-python`;

          const cppKey =
            `${nextPosition}-cpp`;

          if (
            next[pythonKey] === undefined
          ) {

            next[pythonKey] =
              data.starter_code
                ?.python || "";
          }

          if (
            next[cppKey] === undefined
          ) {

            next[cppKey] =
              data.starter_code
                ?.cpp || "";
          }

          return next;
        }
      );
    }
    catch (err) {

      setError(
        err.message
      );
    }
    finally {

      setActionBusy("");
    }
  }


  async function changeQuestion(
    nextPosition
  ) {

    if (
      nextPosition < 1 ||
      nextPosition > 4
    ) {
      return;
    }

    await loadQuestion(
      sessionId,
      nextPosition
    );
  }


  // ==========================================================
  // RUN CODE
  // ==========================================================

  async function handleRun() {

    if (!currentCode.trim()) {

      setError(
        "Write some code before running it."
      );

      return;
    }

    setActionBusy("run");
    setRunResult(null);
    setError("");

    try {

      const result =
        await runCode(
          sessionId,
          position,
          language,
          currentCode
        );

      setRunResult(
        result
      );
    }
    catch (err) {

      setError(
        err.message
      );
    }
    finally {

      setActionBusy("");
    }
  }


  // ==========================================================
  // SUBMIT CODE
  // ==========================================================

  async function handleSubmit() {

    if (!currentCode.trim()) {

      setError(
        "Write some code before submitting."
      );

      return;
    }

    setActionBusy("submit");
    setSubmitResult(null);
    setHint("");
    setError("");

    try {

      const result =
        await submitCode(
          sessionId,
          position,
          language,
          currentCode
        );

      setSubmitResult(
        result
      );

      setSubmitted(
        previous => ({
          ...previous,
          [position]: true
        })
      );

    }
    catch (err) {

      setError(
        err.message
      );
    }
    finally {

      setActionBusy("");
    }
  }


  // ==========================================================
  // GET AI HINT
  // ==========================================================

  async function handleHint() {

    if (!currentCode.trim()) {

      setError(
        "Write code first so the AI can analyze it."
      );

      return;
    }

    setActionBusy("hint");
    setHint("");
    setError("");

    try {

      const result =
        await getHint(
          sessionId,
          position,
          language,
          currentCode,
        );

      setHint(
        result.hint
      );
    }
    catch (err) {

      setError(
        err.message
      );
    }
    finally {

      setActionBusy("");
    }
  }


  // ==========================================================
  // FINISH INTERVIEW
  // ==========================================================

  async function handleFinish() {

    if (!allSubmitted) {

      setError(
        "Submit all four questions before finishing."
      );

      return;
    }

    setBusy(true);
    setError("");

    try {

      const result =
        await finishInterview(
          sessionId,
        );

      const solutionResults =
        await Promise.all(

          [1, 2, 3, 4].map(
            item =>
              getSolution(
                sessionId,
                item
              )
          )
        );

      setReport(result);

      setSolutions(
        solutionResults
      );

      setScreen(
        "report"
      );
    }
    catch (err) {

      setError(
        err.message
      );
    }
    finally {

      setBusy(false);
    }
  }


  // ==========================================================
  // RESET
  // ==========================================================

  function resetInterview() {

    setScreen("dashboard");
    setCompany("");
    setDifficulty("");
    setSessionId("");
    setQuestion(null);
    setPosition(1);
    setCodes({});
    setSubmitted({});
    setRunResult(null);
    setSubmitResult(null);
    setHint("");
    setReport(null);
    setSolutions([]);
    setRemaining(3600);
    setLanguage("python");
    setError("");
  }


  // ==========================================================
  // AUTH LOADING
  // ==========================================================

  if (authError) {

    return (
      <div className="page-center">

        <div className="fatal-card">

          <XCircle size={40} />

          <h2>
            Authentication failed
          </h2>

          <p>
            {authError}
          </p>

        </div>

      </div>
    );
  }


  if (!profile) {

    return (
      <LoadingScreen
        text="Connecting to AI Pipe..."
      />
    );
  }


  // ==========================================================
  // REPORT PAGE
  // ==========================================================

  if (
    screen === "report" &&
    report
  ) {

    return (
      <div className="app-shell">

        <header className="topbar">

          <div className="brand">

            <div className="brand-logo">
              <Code2 size={23} />
            </div>

            <div>
              <strong>
                InterviewAI
              </strong>

              <span>
                Coding Interview Agent
              </span>
            </div>

          </div>

          <div className="profile-chip">

            <UserRound size={17} />

            <span>
              {profile.email || "Candidate"}
            </span>

          </div>

        </header>


        <main className="report-page">

          <ErrorBanner
            message={error}
            onClose={() => setError("")}
          />


          <section className="report-hero">

            <div className="trophy-circle">
              <Trophy size={43} />
            </div>

            <div>

              <div className="eyebrow">
                Interview completed
              </div>

              <h1>
                Your performance report
              </h1>

              <p>
                {report.company}
                {" · "}
                {report.difficulty}
                {" difficulty"}
              </p>

            </div>

          </section>


          <section className="score-grid">

            <div className="metric-card primary">

              <span>
                Overall Score
              </span>

              <strong>
                {report.score_percent}%
              </strong>

              <small>
                Based on passed test cases
              </small>

            </div>


            <div className="metric-card">

              <span>
                Questions Solved
              </span>

              <strong>
                {report.questions_fully_solved}/4
              </strong>

              <small>
                Fully correct submissions
              </small>

            </div>


            <div className="metric-card">

              <span>
                Tests Passed
              </span>

              <strong>
                {report.tests_passed}/{report.total_tests}
              </strong>

              <small>
                Across all questions
              </small>

            </div>

          </section>


          <section className="report-columns">

            <div className="report-panel">

              <div className="panel-title">

                <Sparkles size={20} />

                <div>
                  <h2>
                    AI Interviewer Report
                  </h2>

                  <p>
                    Personalized feedback powered through AI Pipe
                  </p>
                </div>

              </div>

              <div className="ai-report">

                {report.ai_report
                  ? report.ai_report
                      .split("\n")
                      .map(
                        (line, index) => (
                          <p key={index}>
                            {line || "\u00A0"}
                          </p>
                        )
                      )
                  : (
                    <p>
                      AI report was not available.
                    </p>
                  )
                }

              </div>

            </div>


            <div className="report-panel">

              <div className="panel-title">

                <BarChart3 size={20} />

                <div>
                  <h2>
                    Question Results
                  </h2>

                  <p>
                    Submission-level breakdown
                  </p>
                </div>

              </div>


              <div className="submission-list">

                {report.submissions?.map(
                  (item, index) => (

                    <div
                      className="submission-row"
                      key={item.question_id}
                    >

                      <div className="submission-index">
                        {index + 1}
                      </div>

                      <div className="submission-info">

                        <strong>
                          {item.title}
                        </strong>

                        <span>
                          {item.language === "cpp"
                            ? "C++"
                            : "Python"}
                          {" · "}
                          {item.passed}/{item.total}
                          {" tests"}
                        </span>

                      </div>

                      {item.success
                        ? (
                          <CheckCircle2
                            className="success-icon"
                            size={22}
                          />
                        )
                        : (
                          <XCircle
                            className="failure-icon"
                            size={22}
                          />
                        )
                      }

                    </div>
                  )
                )}

              </div>

            </div>

          </section>


          <section className="solutions-section">

            <div className="section-heading">

              <div>

                <div className="eyebrow">
                  Review
                </div>

                <h2>
                  Official solution approaches
                </h2>

              </div>

              <ShieldCheck size={27} />

            </div>


            <div className="solutions-grid">

              {solutions.map(
                (item, index) => (

                  <article
                    className="solution-card"
                    key={item.id}
                  >

                    <div className="solution-number">
                      Question {index + 1}
                    </div>

                    <h3>
                      {item.title}
                    </h3>

                    <p>
                      {
                        item.solution
                          ?.approach
                      }
                    </p>

                    <div className="complexity-row">

                      <span>
                        <strong>
                          Time
                        </strong>
                        {
                          item.solution
                            ?.time_complexity
                        }
                      </span>

                      <span>
                        <strong>
                          Space
                        </strong>
                        {
                          item.solution
                            ?.space_complexity
                        }
                      </span>

                    </div>

                  </article>
                )
              )}

            </div>

          </section>


          <div className="report-actions">

            <button
              className="secondary-button large"
              onClick={resetInterview}
            >
              <RotateCcw size={18} />

              Start Another Interview
            </button>

          </div>

        </main>

      </div>
    );
  }


  // ==========================================================
  // INTERVIEW PAGE
  // ==========================================================

  if (
    screen === "interview"
  ) {

    if (!question) {

      return (
        <LoadingScreen
          text="Loading interview..."
        />
      );
    }


    return (
      <div className="interview-shell">

        <header className="interview-header">

          <div className="brand compact">

            <div className="brand-logo">
              <Code2 size={21} />
            </div>

            <div>
              <strong>
                InterviewAI
              </strong>

              <span>
                {company}
              </span>
            </div>

          </div>


          <div className="interview-meta">

            <div className="difficulty-pill">
              {difficulty}
            </div>

            <div
              className={
                `timer ${
                  remaining < 300
                    ? "danger"
                    : ""
                }`
              }
            >
              <Clock3 size={18} />

              {formatTime(
                remaining
              )}
            </div>

          </div>


          <div className="header-progress">

            <span>
              {submittedCount}/4 submitted
            </span>

            <div className="mini-progress">

              <div
                style={{
                  width:
                    `${
                      submittedCount
                      / 4
                      * 100
                    }%`
                }}
              />

            </div>

          </div>

        </header>


        <div className="question-nav">

          {[1, 2, 3, 4].map(
            number => (

              <button
                key={number}
                className={[
                  "question-tab",

                  position === number
                    ? "active"
                    : "",

                  submitted[number]
                    ? "done"
                    : ""
                ].join(" ")}
                onClick={
                  () =>
                    changeQuestion(
                      number
                    )
                }
                disabled={
                  actionBusy ===
                  "question"
                }
              >

                {submitted[number]
                  ? (
                    <Check
                      size={15}
                    />
                  )
                  : (
                    <span>
                      {number}
                    </span>
                  )
                }

                Question {number}

              </button>

            )
          )}

        </div>


        <ErrorBanner
          message={error}
          onClose={() => setError("")}
        />


        <main className="interview-layout">

          <section className="problem-pane">

            <div className="problem-scroll">

              <div className="problem-top">

                <div className="question-count">
                  Question {position} of 4
                </div>

                <h1>
                  {question.title}
                </h1>

                <div className="tag-row">

                  <span
                    className="difficulty-tag"
                  >
                    {question.difficulty}
                  </span>

                  {question.topics?.map(
                    topic => (
                      <span
                        className="topic-tag"
                        key={topic}
                      >
                        {topic}
                      </span>
                    )
                  )}

                </div>

              </div>


              <div className="problem-section">

                <h3>
                  Problem
                </h3>

                <p>
                  {
                    question.problem_statement
                  }
                </p>

              </div>


              <div className="problem-section">

                <h3>
                  Examples
                </h3>

                <div className="example-list">

                  {
                    question
                      .visible_test_cases
                      ?.map(
                        (test, index) => (

                          <div
                            className="example-card"
                            key={index}
                          >

                            <div className="example-label">
                              Example {index + 1}
                            </div>

                            <div className="code-line">

                              <strong>
                                Input
                              </strong>

                              <code>
                                {
                                  JSON.stringify(
                                    test.input
                                  )
                                }
                              </code>

                            </div>

                            <div className="code-line">

                              <strong>
                                Output
                              </strong>

                              <code>
                                {
                                  JSON.stringify(
                                    test.expected
                                  )
                                }
                              </code>

                            </div>

                          </div>

                        )
                      )
                  }

                </div>

              </div>


              <div className="problem-section">

                <div className="hint-title">

                  <Lightbulb size={18} />

                  <h3>
                    AI Interviewer Hint
                  </h3>

                </div>

                {!hint && (

                  <div className="hint-empty">

                    <p>
                      Stuck? The AI interviewer can inspect
                      your current code and give you a hint
                      without revealing the complete answer.
                    </p>

                    <button
                      className="hint-button"
                      onClick={handleHint}
                      disabled={
                        actionBusy ===
                        "hint"
                      }
                    >

                      {actionBusy === "hint"
                        ? (
                          <LoaderCircle
                            size={17}
                            className="spin"
                          />
                        )
                        : (
                          <Sparkles
                            size={17}
                          />
                        )
                      }

                      Generate Hint

                    </button>

                  </div>

                )}


                {hint && (

                  <div className="hint-box">

                    <Sparkles
                      size={20}
                    />

                    <p>
                      {hint}
                    </p>

                  </div>

                )}

              </div>

            </div>

          </section>


          <section className="editor-pane">

            <div className="editor-toolbar">

              <div className="language-selector">

                <Terminal size={18} />

                <button
                  className={
                    language === "python"
                      ? "selected"
                      : ""
                  }
                  onClick={
                    () =>
                      setLanguage(
                        "python"
                      )
                  }
                >
                  Python
                </button>

                <button
                  className={
                    language === "cpp"
                      ? "selected"
                      : ""
                  }
                  onClick={
                    () =>
                      setLanguage(
                        "cpp"
                      )
                  }
                >
                  C++
                </button>

              </div>


              <div className="editor-question-state">

                {submitted[position]
                  ? (
                    <>
                      <CheckCircle2
                        size={17}
                      />
                      Submitted
                    </>
                  )
                  : (
                    <>
                      <Code2
                        size={17}
                      />
                      In progress
                    </>
                  )
                }

              </div>

            </div>


            <div className="editor-container">

              <Editor
                height="100%"
                theme="vs-dark"
                language={
                  language === "cpp"
                    ? "cpp"
                    : "python"
                }
                value={
                  currentCode
                }
                onChange={
                  value => {

                    setCodes(
                      previous => ({
                        ...previous,
                        [codeKey]:
                          value || ""
                      })
                    );

                  }
                }
                options={{
                  minimap: {
                    enabled: false
                  },

                  fontSize: 15,

                  lineHeight: 23,

                  automaticLayout: true,

                  scrollBeyondLastLine:
                    false,

                  padding: {
                    top: 18
                  },

                  fontLigatures: true,

                  tabSize: 4,

                  wordWrap: "on"
                }}
              />

            </div>


            <div className="result-panel">

              {!runResult &&
                !submitResult && (

                  <div className="result-empty">

                    <Terminal
                      size={19}
                    />

                    <span>
                      Run your code to see
                      visible test results.
                    </span>

                  </div>

                )}


              {runResult && (

                <div className="test-results">

                  <div className="result-heading">

                    <strong>
                      Run Results
                    </strong>

                    <span>
                      {
                        runResult.passed
                      }
                      /
                      {
                        runResult.total
                      }
                      {" passed"}
                    </span>

                  </div>


                  <div className="test-grid">

                    {
                      runResult.tests
                        ?.map(
                          test => (

                            <div
                              className={
                                `test-result ${
                                  test.passed
                                    ? "passed"
                                    : "failed"
                                }`
                              }
                              key={test.test}
                            >

                              <div>

                                {test.passed
                                  ? (
                                    <CheckCircle2
                                      size={17}
                                    />
                                  )
                                  : (
                                    <XCircle
                                      size={17}
                                    />
                                  )
                                }

                                Test {test.test}

                              </div>

                              {
                                test.error &&
                                (
                                  <code>
                                    {test.error}
                                  </code>
                                )
                              }

                              {
                                !test.error &&
                                (
                                  <small>

                                    Output: {
                                      JSON.stringify(
                                        test.actual
                                      )
                                    }

                                  </small>
                                )
                              }

                            </div>

                          )
                        )
                    }

                  </div>

                </div>

              )}


              {submitResult && (

                <div
                  className={
                    `submission-result ${
                      submitResult.success
                        ? "success"
                        : "failure"
                    }`
                  }
                >

                  {submitResult.success
                    ? (
                      <CheckCircle2
                        size={21}
                      />
                    )
                    : (
                      <XCircle
                        size={21}
                      />
                    )
                  }

                  <div>

                    <strong>

                      {
                        submitResult.success
                          ? "Accepted"
                          : "Not Accepted"
                      }

                    </strong>

                    <span>

                      {
                        submitResult.error
                          ? submitResult.error
                          : `${submitResult.passed}/${submitResult.total} hidden + visible tests passed`
                      }

                    </span>

                  </div>

                </div>

              )}

            </div>


            <div className="editor-actions">

              <button
                className="run-button"
                onClick={handleRun}
                disabled={
                  Boolean(
                    actionBusy
                  )
                }
              >

                {actionBusy === "run"
                  ? (
                    <LoaderCircle
                      size={18}
                      className="spin"
                    />
                  )
                  : (
                    <Play
                      size={18}
                    />
                  )
                }

                Run Code

              </button>


              <button
                className="submit-button"
                onClick={handleSubmit}
                disabled={
                  Boolean(
                    actionBusy
                  )
                }
              >

                {actionBusy === "submit"
                  ? (
                    <LoaderCircle
                      size={18}
                      className="spin"
                    />
                  )
                  : (
                    <Send
                      size={18}
                    />
                  )
                }

                {
                  submitted[position]
                    ? "Resubmit"
                    : "Submit"
                }

              </button>

            </div>


            <div className="bottom-navigation">

              <button
                onClick={
                  () =>
                    changeQuestion(
                      position - 1
                    )
                }
                disabled={
                  position === 1 ||
                  Boolean(
                    actionBusy
                  )
                }
              >

                <ArrowLeft
                  size={17}
                />

                Previous

              </button>


              {position < 4 && (

                <button
                  onClick={
                    () =>
                      changeQuestion(
                        position + 1
                      )
                  }
                  disabled={
                    Boolean(
                      actionBusy
                    )
                  }
                >

                  Next

                  <ArrowRight
                    size={17}
                  />

                </button>

              )}


              {position === 4 && (

                <button
                  className={
                    allSubmitted
                      ? "finish-ready"
                      : ""
                  }
                  onClick={
                    handleFinish
                  }
                  disabled={
                    !allSubmitted ||
                    busy
                  }
                >

                  {busy
                    ? (
                      <LoaderCircle
                        className="spin"
                        size={17}
                      />
                    )
                    : (
                      <Trophy
                        size={17}
                      />
                    )
                  }

                  Finish Interview

                </button>

              )}

            </div>

          </section>

        </main>

      </div>
    );
  }


  // ==========================================================
  // DIFFICULTY PAGE
  // ==========================================================

  if (
    screen === "difficulty"
  ) {

    return (
      <div className="app-shell">

        <header className="topbar">

          <div className="brand">

            <div className="brand-logo">
              <Code2 size={23} />
            </div>

            <div>
              <strong>
                InterviewAI
              </strong>

              <span>
                Coding Interview Agent
              </span>
            </div>

          </div>


          <div className="profile-chip">

            <UserRound
              size={17}
            />

            <span>
              {
                profile.email ||
                "Candidate"
              }
            </span>

          </div>

        </header>


        <main className="selection-page">

          <ErrorBanner
            message={error}
            onClose={() => setError("")}
          />


          <button
            className="back-button"
            onClick={
              () =>
                setScreen(
                  "dashboard"
                )
            }
          >

            <ArrowLeft
              size={17}
            />

            Change company

          </button>


          <div className="selection-header">

            <div className="eyebrow">
              Step 2 of 2
            </div>

            <h1>
              Choose your difficulty
            </h1>

            <p>
              Your {company} interview will contain
              four questions from the selected level.
            </p>

          </div>


          <div className="difficulty-grid">

            {
              DIFFICULTIES.map(
                item => {

                  const Icon =
                    item.icon;

                  const selected =
                    difficulty ===
                    item.name;

                  return (

                    <button
                      className={
                        `difficulty-card ${
                          selected
                            ? "selected"
                            : ""
                        }`
                      }
                      key={item.name}
                      onClick={
                        () =>
                          setDifficulty(
                            item.name
                          )
                      }
                    >

                      <div className="difficulty-icon">
                        <Icon size={28} />
                      </div>

                      <h3>
                        {item.name}
                      </h3>

                      <p>
                        {
                          item.description
                        }
                      </p>

                      <div className="selection-check">

                        {selected &&
                          <Check
                            size={16}
                          />
                        }

                      </div>

                    </button>

                  );
                }
              )
            }

          </div>


          <div className="interview-summary">

            <div>

              <BriefcaseBusiness
                size={20}
              />

              <span>
                Company
              </span>

              <strong>
                {company}
              </strong>

            </div>


            <div>

              <Code2
                size={20}
              />

              <span>
                Questions
              </span>

              <strong>
                4
              </strong>

            </div>


            <div>

              <Clock3
                size={20}
              />

              <span>
                Duration
              </span>

              <strong>
                60 min
              </strong>

            </div>

          </div>


          <button
            className="primary-cta"
            disabled={
              !difficulty ||
              busy
            }
            onClick={
              beginInterview
            }
          >

            {busy
              ? (
                <LoaderCircle
                  className="spin"
                  size={20}
                />
              )
              : (
                <Play
                  size={20}
                />
              )
            }

            Start Interview

            <ChevronRight
              size={20}
            />

          </button>

        </main>

      </div>
    );
  }


  // ==========================================================
  // DASHBOARD
  // ==========================================================

  return (
    <div className="app-shell">

      <header className="topbar">

        <div className="brand">

          <div className="brand-logo">
            <Code2 size={23} />
          </div>

          <div>
            <strong>
              InterviewAI
            </strong>

            <span>
              Coding Interview Agent
            </span>
          </div>

        </div>


        <div className="profile-chip">

          <div className="online-dot" />

          <UserRound
            size={17}
          />

          <span>
            {
              profile.email ||
              "Candidate"
            }
          </span>

        </div>

      </header>


      <main className="dashboard">

        <ErrorBanner
          message={error}
          onClose={() => setError("")}
        />


        <section className="dashboard-hero">

          <div className="hero-badge">

            <Sparkles
              size={16}
            />

            AI-powered technical interviews

          </div>

          <h1>
            Practice like it's the
            <span> real interview.</span>
          </h1>

          <p>
            Choose a company and test yourself
            against company-targeted DSA questions
            with code execution, AI hints and a
            personalized final report.
          </p>


          <div className="hero-stats">

            <div>
              <strong>
                60
              </strong>
              <span>
                Curated questions
              </span>
            </div>

            <div>
              <strong>
                5
              </strong>
              <span>
                Companies
              </span>
            </div>

            <div>
              <strong>
                300
              </strong>
              <span>
                Test cases
              </span>
            </div>

            <div>
              <strong>
                AI
              </strong>
              <span>
                Contextual hints
              </span>
            </div>

          </div>

        </section>


        <section className="company-section">

          <div className="section-heading">

            <div>

              <div className="eyebrow">
                Step 1 of 2
              </div>

              <h2>
                Select your target company
              </h2>

            </div>

            <span className="company-count">
              {companies.length || 5} available
            </span>

          </div>


          <div className="company-grid">

            {
              (
                companies.length
                  ? companies
                  : Object.keys(
                      COMPANY_INFO
                    )
              ).map(
                item => {

                  const info =
                    COMPANY_INFO[item] ||
                    {
                      icon:
                        item.slice(0, 2),
                      description:
                        "Technical interview practice",
                      accent:
                        "default"
                    };

                  return (

                    <button
                      className="company-card"
                      key={item}
                      onClick={
                        () => {

                          setCompany(
                            item
                          );

                          setDifficulty(
                            ""
                          );

                          setScreen(
                            "difficulty"
                          );

                        }
                      }
                    >

                      <div
                        className={
                          `company-logo ${info.accent}`
                        }
                      >
                        {
                          info.icon
                        }
                      </div>


                      <div className="company-content">

                        <h3>
                          {item}
                        </h3>

                        <p>
                          {
                            info.description
                          }
                        </p>

                      </div>


                      <div className="company-arrow">

                        <ChevronRight
                          size={20}
                        />

                      </div>

                    </button>

                  );
                }
              )
            }

          </div>

        </section>


        <section className="feature-strip">

          <div>

            <div className="feature-icon">
              <Terminal size={21} />
            </div>

            <span>
              <strong>
                Real code execution
              </strong>

              Python and C++ support
            </span>

          </div>


          <div>

            <div className="feature-icon">
              <Brain size={21} />
            </div>

            <span>
              <strong>
                Adaptive AI hints
              </strong>

              Based on your current code
            </span>

          </div>


          <div>

            <div className="feature-icon">
              <BarChart3 size={21} />
            </div>

            <span>
              <strong>
                Performance report
              </strong>

              Actionable interview feedback
            </span>

          </div>

        </section>

      </main>

    </div>
  );
}


export default App;
