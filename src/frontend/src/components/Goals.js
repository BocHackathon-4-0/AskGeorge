import React from 'react';
import './Goals.css';

function Goals({ goals }) {
    return (
        <div className="goals-container">
            <div className="goals-header">Goals</div> {/* Adding the header here */}
            {goals.map((goal, idx) => (
                <div key={idx} className="goal-card">
                    <div className="goal-title">{goal.title}</div>
                    <div className="progress-bar">
                        <div
                            className="progress-bar-filled"
                            style={{ width: `${(goal.savedAmount / goal.goalAmount) * 100}%` }}
                        ></div>
                    </div>
                    <div className="goal-info">
                        €{goal.savedAmount} of €{goal.goalAmount}
                    </div>
                </div>
            ))}
        </div>
    );
}

export default Goals;
