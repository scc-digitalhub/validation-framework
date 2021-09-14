import * as React from 'react';
import './severity_indicator.css';

export const SeverityIndicator = ({
    level
}) => {
    let toFill = 0;
    if (level > 0)
        toFill = level;
    
    let i = 1;
    let notches = [];
    let classToPush = "severity_notch severity_notch_filled";
    while (i <= 5) {
        if (i > toFill)
            classToPush = "severity_notch severity_notch_empty";
        
        notches.push(<span className={classToPush}></span>);
        
        i++;
    }
    
    return (
        <div className="severity_indicator">
            {notches}
        </div>
    );
};