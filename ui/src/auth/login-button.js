import React, { useEffect, useCallback } from 'react';
import { useSafeSetState, useLogin, useNotify } from 'react-admin'
import PropTypes from 'prop-types';
import { Button, CardActions, CircularProgress, makeStyles } from '@material-ui/core';

const useStyles = makeStyles(
    (theme) => ({
        button: {
            width: '100%',
        },
        icon: {
            marginRight: theme.spacing(1),
        },
    }),
    { name: 'RaLoginButton' }
);

export function LoginButton({
    redirectTo,
    ...rest
}) {
    const classes = useStyles();
    const login = useLogin();
    const notify = useNotify();
    const [loading, setLoading] = useSafeSetState(false);

    const handleLogin = useCallback((code, state) => {
        setLoading(true)
        login({ code, state })
            .catch(error => { notify(error, 'error') })
    }, [login, notify, setLoading]);


    useEffect(() => {
        //extract params from URI
        ///note: it needs a parseable href, disable # history
        const { searchParams } = new URL(window.location.href);
        const code = searchParams.get('code');
        const state = searchParams.get('state');
        const error = searchParams.get('error');
        var error_description = searchParams.get('error_description');

        if (error) {
            if (!error_description) {
                error_description = 'Login error';
            }

            notify(error_description, 'error');
        }


        if (code && state) {
            handleLogin(code, state);
        }
    }, [notify, handleLogin])

    return (
        <CardActions>
            <Button
                {...rest}
                onClick={handleLogin}
                variant="contained"
                color="primary"
                disabled={loading}
                className={classes.button}
            >
                {loading && (
                    <CircularProgress
                        className={classes.icon}
                        size={18}
                        thickness={2}
                    />
                )}
              Login with OAuth2
            </Button>
        </CardActions>

    );
};

LoginButton.propTypes = {
    redirectTo: PropTypes.string,
};

LoginButton.defaultProps = {
    redirectTo: '/'
}