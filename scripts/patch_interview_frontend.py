from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

file = (
    ROOT
    / "frontend"
    / "src"
    / "InterviewApp.jsx"
)

text = file.read_text(
    encoding="utf-8-sig"
)


old = """  useEffect(() => {

    setProfile({
      email: "Candidate"
    });

  }, []);
"""


new = """  useEffect(() => {

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
"""


text = text.replace(
    old,
    new
)


text = text.replace(
    """          profile.token
        );""",
    """        );"""
)


file.write_text(
    text,
    encoding="utf-8"
)

print(
    "Interview app patched."
)