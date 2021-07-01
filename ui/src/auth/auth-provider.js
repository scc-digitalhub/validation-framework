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
            const username = json.username;
            const identity = {
                id: "",
                fullName: username,
                avatar: null,

            };
            return Promise.resolve(identity);
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