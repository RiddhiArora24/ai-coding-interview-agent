import {
  useEffect,
  useState
} from "react";

import {
  ArrowLeft,
  BarChart3,
  Brain,
  CheckCircle2,
  Clock3,
  Code2,
  Eye,
  EyeOff,
  History,
  LoaderCircle,
  LockKeyhole,
  LogIn,
  LogOut,
  Mail,
  Trophy,
  User,
  UserPlus
} from "lucide-react";

import InterviewApp from "./InterviewApp";

import {
  getMe,
  getReports,
  login,
  signup
} from "./api";


function AuthPage({
  onAuthenticated
}) {

  const [mode, setMode] =
    useState("login");

  const [name, setName] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [showPassword, setShowPassword] =
    useState(false);

  const [error, setError] =
    useState("");

  const [busy, setBusy] =
    useState(false);


  async function submit(
    event
  ) {

    event.preventDefault();

    setError("");
    setBusy(true);

    try {

      let result;

      if (mode === "signup") {

        result = await signup(
          name,
          email,
          password
        );

      } else {

        result = await login(
          email,
          password
        );
      }

      localStorage.setItem(
        "auth_token",
        result.token
      );

      localStorage.setItem(
        "auth_user",
        JSON.stringify(
          result.user
        )
      );

      onAuthenticated(
        result.user
      );

    } catch (err) {

      setError(
        err.message
      );

    } finally {

      setBusy(false);
    }
  }


  return (
    <div className="auth-page">

      <div className="auth-background auth-background-one" />
      <div className="auth-background auth-background-two" />


      <div className="auth-brand">

        <div className="brand-logo">
          <Code2 size={24} />
        </div>

        <div>

          <strong>
            InterviewAI
          </strong>

          <span>
            AI Coding Interview Agent
          </span>

        </div>

      </div>


      <div className="auth-layout">

        <section className="auth-copy">

          <div className="auth-badge">

            <Brain size={16} />

            AI-powered interview preparation

          </div>


          <h1>

            Practice.
            <br />

            Improve.
            <br />

            <span>
              Get hired.
            </span>

          </h1>


          <p>

            Practice company-targeted coding
            interviews with real code execution,
            contextual AI hints and persistent
            performance reports.

          </p>


          <div className="auth-features">

            <div>
              <CheckCircle2 size={18} />
              60 curated interview questions
            </div>

            <div>
              <CheckCircle2 size={18} />
              Python and C++ execution
            </div>

            <div>
              <CheckCircle2 size={18} />
              AI-generated interview feedback
            </div>

            <div>
              <CheckCircle2 size={18} />
              Your complete interview history
            </div>

          </div>

        </section>


        <section className="auth-card">

          <div className="auth-card-heading">

            <div className="auth-card-icon">

              {mode === "login"
                ? <LogIn size={23} />
                : <UserPlus size={23} />
              }

            </div>


            <h2>

              {mode === "login"
                ? "Welcome back"
                : "Create your account"
              }

            </h2>


            <p>

              {mode === "login"
                ? "Continue your interview preparation."
                : "Start tracking your interview progress."
              }

            </p>

          </div>


          {error && (

            <div className="auth-error">
              {error}
            </div>

          )}


          <form
            onSubmit={submit}
            className="auth-form"
          >

            {mode === "signup" && (

              <label>

                <span>
                  Name
                </span>

                <div className="auth-input">

                  <User size={17} />

                  <input
                    type="text"
                    placeholder="Your name"
                    value={name}
                    required
                    minLength={2}
                    onChange={
                      e =>
                        setName(
                          e.target.value
                        )
                    }
                  />

                </div>

              </label>

            )}


            <label>

              <span>
                Email address
              </span>

              <div className="auth-input">

                <Mail size={17} />

                <input
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  required
                  onChange={
                    e =>
                      setEmail(
                        e.target.value
                      )
                  }
                />

              </div>

            </label>


            <label>

              <span>
                Password
              </span>

              <div className="auth-input">

                <LockKeyhole size={17} />

                <input
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="Minimum 6 characters"
                  value={password}
                  required
                  minLength={6}
                  onChange={
                    e =>
                      setPassword(
                        e.target.value
                      )
                  }
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={
                    () =>
                      setShowPassword(
                        current =>
                          !current
                      )
                  }
                >

                  {showPassword
                    ? <EyeOff size={17} />
                    : <Eye size={17} />
                  }

                </button>

              </div>

            </label>


            <button
              className="auth-submit"
              disabled={busy}
            >

              {busy
                ? (
                  <LoaderCircle
                    size={19}
                    className="spin"
                  />
                )
                : (
                  mode === "login"
                    ? <LogIn size={19} />
                    : <UserPlus size={19} />
                )
              }


              {mode === "login"
                ? "Sign In"
                : "Create Account"
              }

            </button>

          </form>


          <div className="auth-switch">

            {mode === "login"
              ? "Don't have an account?"
              : "Already have an account?"
            }


            <button
              type="button"
              onClick={
                () => {

                  setError("");

                  setMode(
                    mode === "login"
                      ? "signup"
                      : "login"
                  );
                }
              }
            >

              {mode === "login"
                ? "Create one"
                : "Sign in"
              }

            </button>

          </div>

        </section>

      </div>

    </div>
  );
}


function HistoryPage({
  user,
  onBack,
  onLogout
}) {

  const [reports, setReports] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  useEffect(() => {

    async function load() {

      try {

        const data =
          await getReports();

        setReports(
          data.reports || []
        );

      } catch (err) {

        setError(
          err.message
        );

      } finally {

        setLoading(false);
      }
    }

    load();

  }, []);


  return (
    <div className="history-page">

      <header className="history-header">

        <div className="brand">

          <div className="brand-logo">
            <Code2 size={22} />
          </div>

          <div>

            <strong>
              InterviewAI
            </strong>

            <span>
              Interview History
            </span>

          </div>

        </div>


        <div className="history-user">

          <div>

            <strong>
              {user.name}
            </strong>

            <span>
              {user.email}
            </span>

          </div>


          <button
            onClick={onLogout}
            title="Logout"
          >
            <LogOut size={18} />
          </button>

        </div>

      </header>


      <main className="history-content">

        <button
          className="history-back"
          onClick={onBack}
        >

          <ArrowLeft size={17} />

          Back to Dashboard

        </button>


        <div className="history-title">

          <div>

            <div className="eyebrow">
              Your progress
            </div>

            <h1>
              Interview History
            </h1>

            <p>

              Review your previous coding
              interviews and track how your
              performance changes over time.

            </p>

          </div>


          <div className="history-count">

            <History size={21} />

            <strong>
              {reports.length}
            </strong>

            <span>
              Interviews
            </span>

          </div>

        </div>


        {error && (

          <div className="auth-error">
            {error}
          </div>

        )}


        {loading && (

          <div className="history-loading">

            <LoaderCircle
              className="spin"
              size={25}
            />

            Loading reports...

          </div>

        )}


        {!loading &&
          reports.length === 0 && (

          <div className="history-empty">

            <div>
              <BarChart3 size={42} />
            </div>

            <h2>
              No interview reports yet
            </h2>

            <p>

              Complete your first four-question
              interview and the report will
              automatically appear here.

            </p>

            <button
              onClick={onBack}
            >
              Start an Interview
            </button>

          </div>

        )}


        {!loading &&
          reports.length > 0 && (

          <div className="history-list">

            {reports.map(
              report => {

                const created =
                  new Date(
                    report.created_at
                  );

                return (

                  <article
                    className="history-card"
                    key={report.id}
                  >

                    <div className="history-card-main">

                      <div className="history-company">

                        <div className="history-company-logo">

                          {
                            report.company
                              .slice(0, 2)
                              .toUpperCase()
                          }

                        </div>


                        <div>

                          <h3>
                            {report.company}
                          </h3>

                          <span>
                            {report.difficulty}
                            {" · "}
                            {
                              created.toLocaleDateString()
                            }
                          </span>

                        </div>

                      </div>


                      <div className="history-score">

                        <span>
                          Score
                        </span>

                        <strong>
                          {
                            Number(
                              report.score_percent
                            ).toFixed(0)
                          }%
                        </strong>

                      </div>

                    </div>


                    <div className="history-metrics">

                      <div>

                        <Trophy size={17} />

                        <span>
                          Questions solved
                        </span>

                        <strong>
                          {
                            report.questions_fully_solved
                          }
                          /4
                        </strong>

                      </div>


                      <div>

                        <CheckCircle2 size={17} />

                        <span>
                          Tests passed
                        </span>

                        <strong>
                          {
                            report.tests_passed
                          }
                          /
                          {
                            report.total_tests
                          }
                        </strong>

                      </div>


                      <div>

                        <Clock3 size={17} />

                        <span>
                          Date
                        </span>

                        <strong>
                          {
                            created.toLocaleDateString(
                              undefined,
                              {
                                month: "short",
                                day: "numeric",
                                year: "numeric"
                              }
                            )
                          }
                        </strong>

                      </div>

                    </div>


                    {report.ai_report && (

                      <details className="history-ai">

                        <summary>
                          View AI feedback
                        </summary>

                        <div>
                          {
                            report.ai_report
                          }
                        </div>

                      </details>

                    )}

                  </article>

                );
              }
            )}

          </div>

        )}

      </main>

    </div>
  );
}


function App() {

  const [user, setUser] =
    useState(null);

  const [checking, setChecking] =
    useState(true);

  const [page, setPage] =
    useState("interview");


  useEffect(() => {

    async function check() {

      const token =
        localStorage.getItem(
          "auth_token"
        );

      if (!token) {

        setChecking(false);
        return;
      }

      try {

        const current =
          await getMe();

        localStorage.setItem(
          "auth_user",
          JSON.stringify(
            current
          )
        );

        setUser(
          current
        );

      } catch {

        localStorage.removeItem(
          "auth_token"
        );

        localStorage.removeItem(
          "auth_user"
        );

      } finally {

        setChecking(false);
      }
    }

    check();

  }, []);


  function logout() {

    localStorage.removeItem(
      "auth_token"
    );

    localStorage.removeItem(
      "auth_user"
    );

    setUser(null);

    setPage(
      "interview"
    );
  }


  if (checking) {

    return (
      <div className="page-center">

        <div className="loading-card">

          <LoaderCircle
            size={30}
            className="spin"
          />

          Checking login...

        </div>

      </div>
    );
  }


  if (!user) {

    return (
      <AuthPage
        onAuthenticated={
          current => {

            setUser(
              current
            );

            setPage(
              "interview"
            );
          }
        }
      />
    );
  }


  if (page === "history") {

    return (
      <HistoryPage
        user={user}
        onBack={
          () =>
            setPage(
              "interview"
            )
        }
        onLogout={logout}
      />
    );
  }


  return (
    <div className="authenticated-app">

      <InterviewApp />


      <div className="account-controls">

        <button
          onClick={
            () =>
              setPage(
                "history"
              )
          }
        >

          <History size={17} />

          History

        </button>


        <div className="account-divider" />


        <div className="account-name">

          <User size={16} />

          <span>
            {user.name}
          </span>

        </div>


        <button
          className="logout-control"
          onClick={logout}
          title="Logout"
        >

          <LogOut size={17} />

        </button>

      </div>

    </div>
  );
}


export default App;