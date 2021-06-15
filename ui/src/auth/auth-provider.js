import { UserManager, WebStorageStateStore } from 'oidc-client';

const issuer = 'https://aac.kube-test.smartcommunitylab.it';
const clientId = '1fe78b68-de8e-448b-9591-e74587a3d543';
let redirectUri = '/login';
const scopes = 'openid, profile, user.roles.me';

if (!redirectUri.startsWith("http")) {
    redirectUri = window.location.origin + redirectUri;
}

const userManager = new UserManager({
    authority: issuer,
    client_id: clientId,
    redirect_uri: redirectUri,
    userStore: new WebStorageStateStore({ store: window.localStorage }),
    response_type: 'code',
    scope: scopes
});

export const authProvider = {
    
  login: async (params = {}) => {
    /*
    * Step 1. ask auth code via redirect flow
    */

    // We need to check that a params object is actually passed otherwise it will fail.
    if (!params || !params.code || !params.state) {
      //redirect for auth flow
      userManager.signinRedirect();
      // Here we reject the request because there is no notification shown, but we can add an object if we want to add logic in the login call.
      return Promise.reject({ message: 'Retrieving code from authentication service.', code: 'oauthRedirect' });
    }


    /*
    * Step 2. exchange auth code for token
    */
    // Remove stale states, this is 
    userManager.clearStaleState();
    await userManager.signinRedirectCallback();
    
    return Promise.resolve();
  },
  
  logout: async () => {
    //remove user info
    await userManager.removeUser();

    return Promise.resolve();
  },
  
  checkError: (error) => {
    const { status } = error;

    if (status && (status === 401 || status === 403)) {
      return Promise.reject();
    }
    return Promise.resolve(error);
  },
  
  checkAuth: async () => {
    //lookup user
    const user = await userManager.getUser();

    if (!user || !user.hasOwnProperty("access_token")) {
      //missing or invalid user
      await userManager.removeUser();
      return Promise.reject()
    }
    //extract jwt and validate locally for expiration
    const jwt = user.access_token;
    const now = new Date();
    
    if (!jwt || !user.expires_at) {
      return Promise.reject();
    }
    
    if (now.getTime() > (user.expires_at * 1000)) {
        return Promise.reject();
    }
    return Promise.resolve();
  },
  
  getPermissions: async (params = {}) => {
    //lookup user
    const user = await userManager.getUser();

    if (!user || !user.hasOwnProperty("access_token")) {
      //missing or invalid user
      await userManager.removeUser();
      return Promise.reject()
    }
    
    return {
      "user": user
    }
  },
  
  getAuth: async () => {
    //lookup user
    const user = await userManager.getUser();

    if (!user || !user.hasOwnProperty("access_token")) {
      //missing or invalid user
      await userManager.removeUser();
      return Promise.reject()
    }

    //extract jwt
    const jwt = user.access_token;
    return Promise.resolve(jwt);
  },
  
  getUser: async () => {
    //lookup user
    const user = await userManager.getUser();

    if (!user || !user.hasOwnProperty("access_token")) {
      //missing or invalid user
      await userManager.removeUser();
      return Promise.reject()
    }

    return user;
  },
};