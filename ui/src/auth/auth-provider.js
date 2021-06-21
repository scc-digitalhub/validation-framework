import { fetchUtils } from 'react-admin';

const backendUrl = process.env.REACT_APP_BACKEND_ADDRESS;
const logoutUrl = backendUrl + '/logout';

let userUri = '/user';
if (!userUri.startsWith("http")) {
    userUri = window.location.origin + userUri;
}

const httpClient = (url, options = {}) => {
    return fetchUtils.fetchJson(url, options);
};

export const AuthProvider = {
    logout: async () => {
        const options = {
            method: 'POST',
            headers: new Headers({ 'Content-Type': 'application/json' })
        };
        
        await httpClient(logoutUrl, options);
        window.location.replace(logoutUrl);
    },
    
    getIdentity: async () => {
        const options = {
            method: 'GET',
            headers: new Headers({ 'Accept': 'application/json' })
        };
        
        return httpClient(userUri, options).then( ({ json }) => {
            let id = null;
            let fullName = null;
            let avatar = null;
            
            if (json.principal && json.principal.attributes && json.principal.attributes.sub)
                id = json.principal.attributes.sub;
            
            if (json.principal && json.principal.attributes && json.principal.attributes.preferred_username)
                fullName = json.principal.attributes.preferred_username;
            
            return Promise.resolve({id, fullName, avatar});
        });
        
    },
    
    login: (params) => {
        return Promise.resolve();
    },
  
    checkError: (error) => {
        return Promise.resolve();
    },
  
    checkAuth: (params) => {
        return Promise.resolve();
    },
    
    getPermissions: (params) => {
        return Promise.resolve();
    },
};