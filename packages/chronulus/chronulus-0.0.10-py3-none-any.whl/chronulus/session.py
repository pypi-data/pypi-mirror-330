# MIT License
#
# Copyright (c) 2024 Chronulus AI Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Optional

import requests
from chronulus_core.types.risk import Scorecard

from .environment import BaseEnv, Env, get_default_headers
from chronulus_core.types.response import SessionScorecardResponse, SessionCreationResponse, SessionGetResponse


class Session(BaseEnv):
    """
    A class to manage API sessions for handling specific situations and tasks.

    Parameters
    ----------
    name : str
        The name identifier for the session.
    situation : str
        The context or situation description for the session.
    task : str
        The task to be performed in this session.
    session_id : str, optional
        Unique identifier for an existing session. If None, a new session will be created.
    env : dict, optional
        Environment configuration dictionary. If None, default environment will be used.
    verbose : bool, optional
            Print feedback to stdout if True. Default: True

    Attributes
    ----------
    session_version : str
        Version string for the Session. Set to "1".
    name : str
        The name identifier for the session.
    situation : str
        The context or situation description.
    task : str
        The task description.
    session_id : str
        Unique identifier for the session.
    """

    session_version = "1"

    def __init__(self, name: str, situation: str, task: str, session_id: Optional[str] = None, env: Optional[dict] = None, verbose: bool = True):
        super().__init__(**(env if env and isinstance(env, dict) else {}))

        self.name = name
        self.situation = situation
        self.task = task
        self.session_id = session_id
        self.scorecard: Optional[Scorecard] = None
        self.verbose = verbose

        if self.session_id is None:
            self.create()

    def create(self):
        """
        Create a new session using the API.

        This method sends a POST request to create a new session with the specified
        name, situation, and task. Upon successful creation, the session_id is
        updated with the response from the API.

        Raises
        ------
        Exception
            If the API key is invalid or not active (403 status code).
            If the session creation fails with any other status code.
        """

        resp = requests.post(
            url=f"{self.env.API_URI}/sessions/{self.session_version}/create",
            headers=self.headers,
            json=dict(
                name=self.name,
                situation=self.situation,
                task=self.task,
                session_id=self.session_id,
            )
        )

        if resp.status_code != 200:
            if resp.status_code == 403:
                raise Exception("Failed to create session. API Key is not valid or not yet active. Please allow up to 1 minute for activation of new keys.")
            else:
                raise Exception(f"Failed to create session with status code: {resp.status_code}")
        else:
            session_response = SessionCreationResponse(**resp.json())
            self.session_id = session_response.session_id
            if self.verbose:
                print(f"Session created with session_id: {self.session_id}")
                if session_response.flagged:
                    print(session_response.message)

    def risk_scorecard(self, width: str = "800px") -> str:
        """
        Retrieves the risk scorecard for the current session

        This method retrieves the risk scorecard (Rostami-Tabar et al., 2024) for the current session and returns an
        HTML formatted representation of the risk scorecard. HTML can be easily open in a browser, embedded in Markdown,
        or displayed inline Jupyter notebooks.

        **Example**

        ```python
        from IPython.display import Markdown, display
        scorecard_html = session.risk_scorecard()
        display(Markdown(scorecard_html))
        ```

        Citations
        ---------
        Rostami-Tabar, B., Greene, T., Shmueli, G., & Hyndman, R. J.
        (2024). Responsible forecasting: identifying and typifying forecasting harms.
        arXiv preprint arXiv:2411.16531.


        Parameters
        ----------
        width : str
            Width of the generated context following CSS format. Default is "800px".
            
        """

        if self.scorecard is None:
            self._fetch_scorecard()

        table_header = "<thead><tr><th>Risk Category</th><th>Score</th><th>Risk Factors</th></tr></thead>"
        body_rows = ""
        scores = []
        out_of = []
        for cat in self.scorecard.categories:
            risks = [f"<li>{risk}</li>" for risk in cat.risks]
            risk_list = f"<ul>{''.join(risks)}</ul>"
            row = f"<tr><td>{cat.name}</td><td>{cat.score} / {cat.max_score:.1f}</td><td>{risk_list}</td></tr>"
            body_rows += row
            scores.append(cat.score)
            out_of.append(cat.max_score)

        total = float(sum(scores))
        possible = float(sum(out_of))
        max_score = max(scores)

        table_body = f"<tbody>{body_rows}</tbody"

        assessment = f"<h3>Risk Assessment</h3><h5>Overall Score: {total:.1f} / {possible:.1f} | Highest: {max_score}</h5><p>{self.scorecard.assessment}</p>"
        recommendations = f"<h3>Recommendations</h3><p>{self.scorecard.recommendation}</p>"

        details = f"<h3>Details</h3><table>{table_header}{table_body}</table>"

        report = f"<div style='max-width:{width}'>{assessment}{recommendations}{details}</div>"

        return report

    def _fetch_scorecard(self):

        if self.verbose:
            print("Fetching the risk scorecard...")

        resp = requests.post(
            url=f"{self.env.API_URI}/sessions/{self.session_version}/get-risk-scorecard",
            headers=self.headers,
            json=dict(
                name=self.name,
                situation=self.situation,
                task=self.task,
                session_id=self.session_id,
            )
        )

        if resp.status_code != 200:
            if resp.status_code == 403:
                raise Exception("Failed to fetch scorecard. API Key is not valid or not yet active. Please allow up to 1 minute for activation of new keys.")
            else:
                raise Exception(f"Failed to fetch scorecard with status code: {resp.status_code}")
        else:
            response_json = resp.json()
            response = SessionScorecardResponse(**response_json)
            self.scorecard = response.scorecard
            if self.verbose:
                print("Scorecard has been retrieved.")

    @staticmethod
    def load_from_saved_session(session_id: str, env: Optional[dict] = None, verbose: bool = True):
        """
        Load an existing session using a session ID.

        Parameters
        ----------
        session_id : str
            The unique identifier of the session to load.
        env : dict, optional
            Environment configuration dictionary. If None, default environment will be used.
        verbose : bool, optional
            Print feedback to stdout if True. Default: True

        Returns
        -------
        Session
            A new Session instance initialized with the saved session data.

        Raises
        ------
        ValueError
            If the session loading fails or if the response cannot be parsed.
        """

        env = env if env and isinstance(env, dict) else {}
        base = BaseEnv(**env)

        resp = requests.post(
            url=f"{base.env.API_URI}/sessions/{Session.session_version}/from-session-id",
            headers=base.headers,
            json=dict(session_id=session_id)
        )

        if resp.status_code != 200:
            raise ValueError(f"Failed to create session with status code: {resp.status_code}, {resp.text}")

        try:
            session_response = SessionGetResponse(**resp.json())
            if session_response.success:
                session = Session(**session_response.session.model_dump(), env=base.env.model_dump(), verbose=verbose)
                if verbose:
                    print(f"Session retrieved with session_id: {session.session_id}")
                return session

            else:
                raise ValueError(session_response.message)

        except Exception as e:
            raise ValueError(f"Failed to parse session response: {resp.text}")



