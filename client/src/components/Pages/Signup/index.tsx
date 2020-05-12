import React from 'react';
import { Redirect, Link as RouterLink } from 'react-router-dom';
import { Formik } from 'formik';
import * as Yup from 'yup';
import Button from '@material-ui/core/Button';
import Link from '@material-ui/core/Link';
import Paper from '@material-ui/core/Paper';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';

import * as ROUTES from '../../utils/routes';
import {
  validateUsername,
  validateEmail,
  validatePassword,
  validatePasswordConfirm,
} from '../../utils/validators';
import { makeStyles, createStyles, Theme, useTheme } from '@material-ui/core';

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
        maxWidth: '500px',
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
          Welcome!
        </Typography>
        <section className={classes.small} style={{ textAlign: 'center' }}>
          Sign up to use livia
        </section>
        <Formik
          initialValues={{
            username: '',
            email: '',
            password: '',
            password2: '',
          }}
          validateOnChange={false}
          validationSchema={Yup.object({
            username: validateUsername(),
            email: validateEmail(),
            password: validatePassword(),
            password2: validatePasswordConfirm(),
          })}
          onSubmit={(values) => console.log(values)}
        >
          {({
            values,
            touched,
            errors,
            handleChange,
            handleBlur,
            handleSubmit,
          }) => (
            <form className={classes.form} onSubmit={handleSubmit}>
              <TextField
                name='username'
                label='Username'
                type='text'
                className={classes.field}
                value={values.username}
                onChange={handleChange}
                onBlur={handleBlur}
                helperText={
                  errors.username && touched.username && errors.username
                }
                error={!!(errors.username && touched.username)}
                fullWidth
              />
              <TextField
                name='email'
                label='Email'
                type='email'
                className={classes.field}
                value={values.email}
                onChange={handleChange}
                onBlur={handleBlur}
                helperText={errors.email && touched.email && errors.email}
                error={!!(touched.email && errors.email)}
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
                helperText={
                  errors.password && touched.password && errors.password
                }
                error={!!(touched.password && errors.password)}
                fullWidth
              />
              <TextField
                name='password2'
                label='Confirm Your Password'
                type='password'
                className={classes.field}
                value={values.password2}
                onChange={handleChange}
                onBlur={handleBlur}
                helperText={
                  errors.password2 && touched.password2 && errors.password2
                }
                error={!!(touched.password2 && errors.password2)}
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
                Sign Up
              </Button>
            </form>
          )}
        </Formik>
        <section style={{ marginTop: '2rem' }} className={classes.small}>
          Already have an account?
          <Link component={RouterLink} to={ROUTES.LOGIN} color='primary'>
            <strong> Login here.</strong>
          </Link>
        </section>
        <section className={classes.small}>
          By clicking the sign up button, you agree to livia's
          <Link component={RouterLink} to={ROUTES.TERMS} color='primary'>
            {' terms and conditions'}
          </Link>
        </section>
      </Paper>
    </div>
  );
}
