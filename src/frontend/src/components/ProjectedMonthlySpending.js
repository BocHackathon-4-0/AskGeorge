import React from 'react';
import './ProjectedMonthlySpending.css';

function ProjectedMonthlySpendingA({ amount }) {
    return (
        <div className="projected-card">
            <div className="projected-title">Projected Monthly Spending</div>
            <div className="projected-amount">€{amount}</div>
        </div>
    );
}

export default ProjectedMonthlySpendingA;
