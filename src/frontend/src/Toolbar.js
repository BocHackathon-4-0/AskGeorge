import React from 'react';
import WeeklyBudget from './WeeklyBudget';
import ProjectedMonthlySpendingA from './ProjectedMonthlySpending';
import Goals from './Goals';

function Toolbar() {
    const goalsData = [
        { title: "Padel Racket", savedAmount: 180, goalAmount: 250 },
        { title: "New Laptop", savedAmount: 200, goalAmount: 800 },
        // ... add more goals
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
