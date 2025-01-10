import React from 'react';
import { render, screen, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QuizPage } from './AddQuizPage';

describe('QuizPage component', () => {
  it('renders without crashing', () => {
    render(<QuizPage />);
  });

  it('renders quiz name field', () => {
    const { getByLabelText } = render(<QuizPage />);
    expect(getByLabelText('Введите название квиза!')).toBeInTheDocument();
  });

  it('renders difficulty level Autocomplete', () => {
    const { getByLabelText } = render(<QuizPage />);
    expect(getByLabelText('Выберите сложность квиза!')).toBeInTheDocument();
  });

  it('adds a new question when add button is clicked', async () => {
    const { getByText, getByLabelText } = render(<QuizPage />);
    const addButton = getByText('+');
    const questionField = getByLabelText('Введите вопрос');

    await act(async () => {
      await userEvent.click(addButton);
      await userEvent.type(questionField, 'What is the capital of France?');
    });

    expect(screen.getByText('What is the capital of France?')).toBeInTheDocument();
  });

  it('submits the quiz when submit button is clicked', async () => {
    window.fetch = jest.fn().mockResolvedValue({
      json: async () => ({ success: true })
    });

    const { getByLabelText, getByText } = render(<QuizPage />);
    const quizNameField = getByLabelText('Введите название квиза!');
    const submitButton = getByText('Отправить');

    await act(async () => {
      await userEvent.type(quizNameField, 'My Awesome Quiz');
      await userEvent.click(submitButton);
    });

    expect(window.fetch).toHaveBeenCalledWith(
      'http://localhost:8080/api/v1/quizzes/add_quiz',
      expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: expect.stringContaining(JSON.stringify({
          quiz_name: 'My Awesome Quiz',
          // ... other fields
        }))
      })
    );

    expect(console.log).toHaveBeenCalledWith(expect.anything());
  });
});