from matrxs.agents.agent_brain import AgentBrain, Message
from matrxs.utils.agent_utils.navigator import Navigator
from matrxs.utils.agent_utils.state_tracker import StateTracker


class PatrollingAgentBrain(AgentBrain):

    def __init__(self, waypoints, knowledge_decay=10, communicate_state_to_team=False):
        super().__init__()
        self.state_tracker = None
        self.navigator = None
        self.waypoints = waypoints
        self._knowledge_decay = knowledge_decay
        self._communicate_state_to_team = communicate_state_to_team
        self._observed_state = {}

    def initialize(self):
        # Initialize this agent's state tracker
        self.state_tracker = StateTracker(agent_id=self.agent_id, knowledge_decay=self._knowledge_decay)

        self.navigator = Navigator(agent_id=self.agent_id, action_set=self.action_set,
                                   algorithm=Navigator.A_STAR_ALGORITHM)

        self.navigator.add_waypoints(self.waypoints, is_circular=True)

    def filter_observations(self, state):

        # Check if we received message containing state information which we append to the state we observed
        self._observed_state = state.copy()
        combined_state = state.copy()
        if len(self.received_messages) > 0:
            for mssg in self.received_messages:
                if isinstance(mssg.content, dict) and "state" in mssg.content.keys() and mssg.from_id != self.agent_id:
                    combined_state = {**combined_state.copy(), **mssg.content['state'].copy()}

        self.state_tracker.update(combined_state)
        memorized_state = self.state_tracker.get_memorized_state()
        return memorized_state

    def decide_on_action(self, state, possible_actions):

        move_action = self.navigator.get_move_action(self.state_tracker)

        # Communicate state if we need to
        if self._communicate_state_to_team:
            team_members = state['World']['team_members']
            for team_member in team_members:
                self.send_message(message_content={"state": self._observed_state}, to_id=team_member)

        return move_action, {}
