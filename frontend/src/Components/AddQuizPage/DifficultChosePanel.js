import Autocomplete from "@mui/material/Autocomplete";
import TextField from "@mui/material/TextField";


function DifficultChoosePanel() {
    const options = ["Простой", "Средний", "Сложный"];
    return (
        <Autocomplete
            id="difficult-level"
            className="difficult-choose"
            disablePortal
            options={options}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Выберите сложность квиза!" />}
        />
    );
}

export default DifficultChoosePanel;