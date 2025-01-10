import ToggleButton from '@mui/material/ToggleButton';
import { styled } from '@mui/material/styles';


const OptionButton = styled(ToggleButton)(() => ({
    checkedBackgroundColor: "#000",
    '&.Mui-selected': {
        color: "#fff",
        backgroundColor: "#000",
    },
}));

export { OptionButton };