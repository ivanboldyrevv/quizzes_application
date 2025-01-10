function Question({questionText, options}) {
    const optionsText = options.map(option => `(${option.option_text}, ${option.is_correct})`).join(" ");
    return (
        <p>{questionText} / {optionsText}</p>
    );
}

export default Question;