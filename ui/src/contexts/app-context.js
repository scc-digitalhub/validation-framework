import * as React from 'react';

export const AppContext = React.createContext({
    getProject: () => {},
    getExperiment: () => {},
    setProject: () => {},
    setExperiment: () => {}
});