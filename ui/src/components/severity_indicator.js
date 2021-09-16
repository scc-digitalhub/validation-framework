import * as React from 'react';
import './severity_indicator.css';

export const SeverityIndicator = ({
    level,
    color
}) => {
    let toFill = 0;
    if (level > 0)
        toFill = level;
    
    let i = 1;
    let notches = [];
    const emptyClass = "severity_notch severity_notch_empty";
    const filledClass = "severity_notch severity_notch_filled";
    const filledStyle = {
        "background-color": "#" + color,
        "border-color": "#" + color
    };
    while (i <= 5) {
        if (i > toFill)
            notches.push(<span className={emptyClass}></span>);
        else
            notches.push(<span className={filledClass} style={filledStyle}></span>);
        
        i++;
    }
    
    return (
        <div className="severity_indicator">
            {notches}
        </div>
    );
};