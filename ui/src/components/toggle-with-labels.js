import * as React from 'react';
import './toggle-with-labels.css';

export const ToggleWithLabels = ({
    toggleName,
    leftLabel,
    rightLabel,
    handleToggle
}) => {
    const toggleCheckbox = () => {
        document.getElementById(toggleName).checked = !(document.getElementById(toggleName).checked);
        handleToggle();
    };
    
    return (
        <div className="toggle_with_labels" onClick={toggleCheckbox}>
            <input type="checkbox" id={toggleName} checked="checked"/>
            <span>{leftLabel}</span>
            <span>{rightLabel}</span>
        </div>
    );
};