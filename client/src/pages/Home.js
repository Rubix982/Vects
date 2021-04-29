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
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';

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

    const inputQuery = React.useRef('');
    const [isQueriedReceived, setIsQueriedReceived] = React.useState(false);

    async function fetchData(query) {
        // You can await here
        await fetch(`http://localhost:80/request?query=${query}`, {
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            mode: 'cors', // no-cors, *cors, same-origin
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // incl ude, *same-origin, omit
            headers: {
                'Content-Type': 'application/json'
                // 'Content-Type': 'application/x-www-form-urlencoded',
            },
            redirect: 'follow', // manual, *follow, error
            referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        })
            .then(response => response.json())
            .then(data => { console.log(data); if (data !== {}) { setIsQueriedReceived(true); } })
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

    function createData(name, calories, fat, carbs, protein) {
        return { name, calories, fat, carbs, protein };
    }

    const rows = [
        createData('Frozen yoghurt', 159, 6.0, 24, 4.0),
        createData('Ice cream sandwich', 237, 9.0, 37, 4.3),
        createData('Eclair', 262, 16.0, 24, 6.0),
        createData('Cupcake', 305, 3.7, 67, 4.3),
        createData('Gingerbread', 356, 16.0, 49, 3.9),
    ];

    function createCheckmarkData(criteria, status) {
        return { criteria, status };
    }

    const checkmarks = [
        createCheckmarkData('Preprocessing', 'true'),
        createCheckmarkData('Formation Of Inverted And Positonal Indexes', 'true'),
        createCheckmarkData('Simple Boolean Queries', 'true'),
        createCheckmarkData('Complex Boolean Queries', 'true'),
        createCheckmarkData('Proximity Queries', 'true'),
        createCheckmarkData('GUI', 'true'),
        createCheckmarkData('Easy To Read Code', 'true'),
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
                    <div className={classes.buttonMargin}>
                        <FormControl component="fieldset">
                            <FormLabel component="legend">Query Type</FormLabel>
                            <RadioGroup row aria-label="position" name="position" defaultValue="top">
                                <FormControlLabel
                                    value="Simple Boolean"
                                    control={<Radio color="primary" />}
                                    label="Boolean"
                                    labelPlacement="end"
                                />
                                <FormControlLabel
                                    value="Complex Boolean"
                                    control={<Radio color="primary" />}
                                    label="Boolean"
                                    labelPlacement="end"
                                />                                
                                <FormControlLabel
                                    value="Proximity Search"
                                    control={<Radio color="primary" />}
                                    label="Proximity"
                                    labelPlacement="end"
                                />
                            </RadioGroup>
                        </FormControl>
                    </div>
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
                                        Dessert (100g serving)
                                    </TableCell>
                                    <TableCell align="left">
                                        Calories
                                    </TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {rows.map((row) => (
                                    <TableRow key={row.name}>
                                        <TableCell component="th" scope="row">
                                            {row.name}
                                        </TableCell>
                                        <TableCell align="left">
                                            {row.calories}
                                        </TableCell>
                                    </TableRow>
                                ))}
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