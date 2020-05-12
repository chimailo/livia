import React from 'react';
import { Redirect, Link as RouterLink } from 'react-router-dom';
import { Formik } from 'formik';
import Button from '@material-ui/core/Button';
import Link from '@material-ui/core/Link';
import Paper from '@material-ui/core/Paper';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';

import * as ROUTES from '../../utils/routes';
import { makeStyles, createStyles, Theme } from '@material-ui/core';

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    background: {
      position: 'static',
      background: `linear-gradient(60deg, ${theme.palette.grey[100]}, ${theme.palette.secondary.main})`,
      [theme.breakpoints.up('sm')]: {
        padding: '3rem 0',
      },
    },
    paper: {
      width: '100%',
      padding: '50px 0',
      boxShadow: theme.shadows[0],
      [theme.breakpoints.up('sm')]: {
        margin: '2rem auto',
        maxWidth: '450px',
        boxShadow: theme.shadows[24],
      },
    },
    form: {
      width: '80%',
      margin: 'auto',
      maxWidth: '300px',
    },
    field: {
      marginTop: '1rem',
    },
    small: {
      color: theme.palette.grey[600],
      marginLeft: 'auto',
      marginRight: 'auto',
      fontSize: '0.75rem',
      maxWidth: '300px',
      marginTop: '0.4rem',
    },
  })
);

export default function SignUp() {
  const classes = useStyles();

  const isAuthenticated = false;
  if (isAuthenticated) {
    return <Redirect to={ROUTES.HOME} />;
  }

  return (
    <div className={classes.background}>
      <Paper className={classes.paper}>
        <Typography align='center' color='primary' variant='h5' noWrap>
          Welcome back!
        </Typography>
        <section className={classes.small} style={{ textAlign: 'center' }}>
          Login to your account
        </section>
        <Formik
          initialValues={{
            username: '',
            email: '',
            password: '',
            password2: '',
          }}
          onSubmit={(values) => console.log(values)}
        >
          {({ values, handleChange, handleBlur, handleSubmit }) => (
            <form className={classes.form} onSubmit={handleSubmit}>
              <TextField
                name='email'
                label='Email'
                type='email'
                className={classes.field}
                value={values.email}
                onChange={handleChange}
                onBlur={handleBlur}
                fullWidth
              />
              <TextField
                name='password'
                label='Password'
                type='password'
                className={classes.field}
                value={values.password}
                onChange={handleChange}
                onBlur={handleBlur}
                fullWidth
              />
              <Button
                type='submit'
                color='primary'
                variant='contained'
                style={{ marginTop: '3rem' }}
                disableElevation
                fullWidth
              >
                Login
              </Button>
            </form>
          )}
        </Formik>
        <section style={{ marginTop: '2rem' }} className={classes.small}>
          Don't have an account?
          <Link component={RouterLink} to={ROUTES.SIGNUP} color='primary'>
            <strong> Sign up here.</strong>
          </Link>
        </section>
      </Paper>
    </div>
  );
}
