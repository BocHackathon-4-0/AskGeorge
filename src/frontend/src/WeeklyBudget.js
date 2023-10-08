import React from 'react';
import './WeeklyBudget.css';

function WeeklyBudget({ goal, spent }) {
    const CIRCUMFERENCE = 2 * Math.PI * 100;  // considering the radius of our circle is 50
    const percentage = Math.min((spent / goal), 1);
    const offset = CIRCUMFERENCE - (percentage * CIRCUMFERENCE);

    return (
        <div className="budget-ring-container">
            <div className="budget-title">Weekly Budget</div>
            <svg className="budget-ring" viewBox="0 0 240 240">
                <circle cx="120" cy="120" r="100" stroke="#e0e0e0" strokeWidth="20" fill="none"/>
                <circle cx="120" cy="120" r="100" stroke="#007bff" strokeWidth="20" fill="none" 
                        strokeDasharray={CIRCUMFERENCE}
                        strokeDashoffset={offset}
                        transform="rotate(-90, 120, 120)"/>
            </svg>
            <div className="budget-details">
                <div className="spent-amount">€{spent}</div>
                <div className="budget-goal">of €{goal}</div>
            </div>
        </div>
    );
}

export default WeeklyBudget;
