import React, { useState, Fragment } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import AppBar from '@material-ui/core/AppBar';
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';
import IconButton from '@material-ui/core/IconButton';
import Link from '@material-ui/core/Link';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import useMediaQuery from '@material-ui/core/useMediaQuery';
import {
  makeStyles,
  createStyles,
  Theme,
  useTheme,
} from '@material-ui/core/styles';
import AccountCircleIcon from '@material-ui/icons/AccountCircle';
import AddIcon from '@material-ui/icons/Add';
import NotificationsIcon from '@material-ui/icons/Notifications';
import * as ROUTES from '../utils/routes';

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      flexGrow: 1,
    },
    margin: {
      [theme.breakpoints.up('sm')]: {
        margin: theme.spacing(1),
      },
    },
    flexEnd: {
      alignItems: 'stretch',
      display: 'flex',
      justifyContent: 'flex-end',
      marginLeft: 'auto',
    },
  })
);

export default function Navigation() {
  const [isAuthenticated, setAuthenticated] = useState(false);

  const classes = useStyles();
  const theme = useTheme();
  const matchesSm = useMediaQuery(theme.breakpoints.down('sm'));

  return (
    <div className={classes.root}>
      <AppBar color='primary' position='static'>
        <Container maxWidth='lg' disableGutters>
          <Toolbar component='nav'>
            <Typography variant='h5' noWrap>
              <Link
                component={RouterLink}
                to={isAuthenticated ? ROUTES.HOME : ROUTES.LANDING}
                color='secondary'
                underline='none'
              >
                Livia
              </Link>
            </Typography>
            <div className={classes.flexEnd}>
              {isAuthenticated ? (
                <Fragment>
                  <IconButton color='secondary' aria-label='toggle theme'>
                    <AddIcon fontSize='small' />
                  </IconButton>
                  <IconButton color='secondary' aria-label='notifiactions'>
                    <NotificationsIcon fontSize='small' />
                  </IconButton>
                  <IconButton color='secondary' aria-label='avater'>
                    <AccountCircleIcon fontSize='small' />
                  </IconButton>
                </Fragment>
              ) : (
                <Fragment>
                  <Button
                    to={ROUTES.SIGNUP}
                    component={RouterLink}
                    className={classes.margin}
                    size={matchesSm ? 'small' : 'medium'}
                    variant='outlined'
                    color='secondary'
                  >
                    Sign up
                  </Button>
                  <Button
                    to={ROUTES.LOGIN}
                    component={RouterLink}
                    className={classes.margin}
                    size={matchesSm ? 'small' : 'medium'}
                    color='secondary'
                  >
                    Login
                  </Button>
                </Fragment>
              )}
            </div>
          </Toolbar>
        </Container>
      </AppBar>
    </div>
  );
}
