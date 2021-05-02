import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import MenuIcon from '@material-ui/icons/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import Menu from '@material-ui/core/Menu';
import IconButton from '@material-ui/core/IconButton';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';

require('dotenv').config();

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
    title: {
        flexGrow: 1,
    },
    centerStyling: {
        margin: 0,
        padding: 0,
        width: '100%',
        height: '100%',
    },
    buttonMargin: {
        marginTop: '20px',
        marginLeft: '20px'
    }
}));

export default function Home({ children }) {

    let data = {}
    let renderData = []
    const inputQuery = React.useRef('');
    const [isQueriedReceived, setIsQueriedReceived] = React.useState(false);

    async function fetchData(query) {

        data = await fetch(`${process.env.REACT_APP_API_ROUTE}/query/${query}`);

        data = await data.json()

        data = data['results']

        for (var key in data) {
            renderData.push({
                key: key,
                value: data[key]
            })
        }

        console.log(renderData)

        setIsQueriedReceived(true);
    }

    const classes = useStyles();
    const [targetEl, setTargetEl] = React.useState(null);
    const openDropDown = Boolean(targetEl);

    const handleDropdown = (event) => {
        setTargetEl(event.currentTarget);
    };

    const handleDropdownClose = () => {
        setTargetEl(null);
    };

    const onSubmitQuery = () => {
        fetchData(inputQuery.current.value);
    };

    function createCheckmarkData(criteria, status) {
        return { criteria, status };
    }

    const checkmarks = [
        createCheckmarkData('Preprocessing', 'true'),
        createCheckmarkData('Formation Of Index', 'true'),
        createCheckmarkData('Code Complexity', 'true'),
        createCheckmarkData('Loading Indexes', 'true'),
        createCheckmarkData('Vector Space Model', 'true'),
        createCheckmarkData('Query Processing', 'true'),
        createCheckmarkData('Code Clarity', 'true'),
        createCheckmarkData('GUI', 'true'),
        createCheckmarkData('GUI is good looking - hopefully!', 'true'),
        createCheckmarkData('Well Commented Code', 'true'),
    ];

    return (
        <div className={classes.root}>
            <AppBar position="static">
                <Toolbar>
                    <IconButton
                        edge="start"
                        className={classes.menuButton}
                        color="inherit"
                        onClick={handleDropdown}
                        aria-label="menu"
                    >
                        <MenuIcon />
                    </IconButton>
                    <Menu
                        id="menu-appbar"
                        anchorEl={targetEl}
                        anchorOrigin={{
                            vertical: 'top',
                            horizontal: 'right',
                        }}
                        keepMounted
                        transformOrigin={{
                            vertical: 'top',
                            horizontal: 'right',
                        }}
                        open={openDropDown}
                        onClose={handleDropdownClose}
                    >
                        <MenuItem onClick={handleDropdownClose}>Home</MenuItem>
                        <MenuItem onClick={handleDropdownClose}>Accomplishments</MenuItem>
                    </Menu>
                    <Typography variant="h6" className={classes.title}>
                        Findex
          </Typography>
                </Toolbar>
            </AppBar>
            {children}
            <div style={{ margin: 'auto', paddingLeft: '20px' }}>
                <form className={classes.root} noValidate autoComplete="off">
                    <TextField size='medium'
                        id="outlined-basic"
                        label="Type your query in here!"
                        inputRef={inputQuery}
                        variant="outlined"
                        style={{
                            marginTop: '20px',
                            maxWidth: 3800
                        }}
                    />
                    <Button onClick={onSubmitQuery} variant="contained" size="large" color="primary" className={classes.buttonMargin}>
                        Query!
                    </Button>
                </form>
            </div>
            <ListItem button>
                <ListItemText primary="" />
            </ListItem>
            <Divider />
            <ListItem button>
                <ListItemText primary="" />
            </ListItem>
            {
                isQueriedReceived &&
                <div>
                    <TableContainer component={Paper}>
                        <Table className={classes.table} aria-label="simple table">
                            <TableHead>
                                <TableRow>
                                    <TableCell>
                                        Document
                                    </TableCell>
                                    <TableCell align="left">
                                        Ranking
                                    </TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {
                                    renderData.map(dataToRender => (                                        
                                        <TableRow key={dataToRender.key}>
                                            <TableCell component="th" scope="row">
                                                {dataToRender.key}
                                            </TableCell>
                                            <TableCell align="left">
                                                {dataToRender.value}
                                            </TableCell>
                                        </TableRow>
                                    ))
                                }
                            </TableBody>
                        </Table>
                    </TableContainer>
                </div>
            }
            <div>
                <TableContainer component={Paper}>
                    <Table className={classes.table} aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell>
                                    Accomplishments
                                    </TableCell>
                                <TableCell align="left">
                                    Checkmarks
                                </TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {checkmarks.map((checkmark) => (
                                <TableRow key={checkmark.name}>
                                    <TableCell component="th" scope="row">
                                        {checkmark.criteria}
                                    </TableCell>
                                    <TableCell align="left">
                                        {checkmark.status === 'true' ? '✅' : '❌'}
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </div>
        </div >
    );
}