const API_BASE =
  import.meta.env.VITE_API_URL || "";


function authToken() {

  return localStorage.getItem(
    "auth_token"
  );
}


async function request(
  path,
  options = {}
) {

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {})
  };

  const token = authToken();

  if (token) {

    headers.Authorization =
      `Bearer ${token}`;
  }

  const response = await fetch(
    `${API_BASE}${path}`,
    {
      ...options,
      headers
    }
  );

  let data = {};

  try {

    data = await response.json();
  }

  catch {
    data = {};
  }

  if (!response.ok) {

    throw new Error(
      data?.detail
      || data?.message
      || `Request failed with ${response.status}`
    );
  }

  return data;
}


export function signup(
  name,
  email,
  password
) {

  return request(
    "/api/auth/signup",
    {
      method: "POST",
      body: JSON.stringify({
        name,
        email,
        password
      })
    }
  );
}


export function login(
  email,
  password
) {

  return request(
    "/api/auth/login",
    {
      method: "POST",
      body: JSON.stringify({
        email,
        password
      })
    }
  );
}


export function getMe() {

  return request(
    "/api/auth/me"
  );
}


export function getReports() {

  return request(
    "/api/reports"
  );
}


export function saveReport(
  report
) {

  return request(
    "/api/reports",
    {
      method: "POST",
      body: JSON.stringify(
        report
      )
    }
  );
}


export function getCompanies() {

  return request(
    "/api/companies"
  );
}


export function startInterview(
  company,
  difficulty
) {

  return request(
    "/api/interviews/start",
    {
      method: "POST",
      body: JSON.stringify({
        company,
        difficulty
      })
    }
  );
}


export function getInterview(
  sessionId
) {

  return request(
    `/api/interviews/${sessionId}`
  );
}


export function getQuestion(
  sessionId,
  position
) {

  return request(
    `/api/interviews/${sessionId}/questions/${position}`
  );
}


export function runCode(
  sessionId,
  position,
  language,
  code
) {

  return request(
    `/api/interviews/${sessionId}/questions/${position}/run`,
    {
      method: "POST",
      body: JSON.stringify({
        language,
        code
      })
    }
  );
}


export function submitCode(
  sessionId,
  position,
  language,
  code
) {

  return request(
    `/api/interviews/${sessionId}/questions/${position}/submit`,
    {
      method: "POST",
      body: JSON.stringify({
        language,
        code
      })
    }
  );
}


export function getHint(
  sessionId,
  position,
  language,
  code
) {

  return request(
    `/api/interviews/${sessionId}/questions/${position}/hint`,
    {
      method: "POST",
      body: JSON.stringify({
        language,
        code
      })
    }
  );
}


export async function finishInterview(
  sessionId
) {

  const result = await request(
    `/api/interviews/${sessionId}/finish`,
    {
      method: "POST"
    }
  );

  try {

    await saveReport(
      result
    );
  }

  catch (error) {

    console.error(
      "Could not save report history:",
      error
    );
  }

  return result;
}


export function getSolution(
  sessionId,
  position
) {

  return request(
    `/api/interviews/${sessionId}/solutions/${position}`
  );
}