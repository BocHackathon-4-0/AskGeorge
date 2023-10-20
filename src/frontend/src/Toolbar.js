import React from 'react';
import WeeklyBudget from './components/WeeklyBudget';
import Goals from './components/Goals';
import ProjectedMonthlySpendingA from './components/ProjectedMonthlySpending';

function Toolbar() {
    const goalsData = [
        { title: "Padel Racket", savedAmount: 180, goalAmount: 250 },
    ];

    return (
        <div className="toolbar">
            <WeeklyBudget goal={800} spent={520} />
            <ProjectedMonthlySpendingA amount={2080} /> {/* Assuming a projection of 4 weeks x $520 */}
            <Goals goals={goalsData}/>
            {/* Add other components here later as needed */}
        </div>
    );
}

export default Toolbar;