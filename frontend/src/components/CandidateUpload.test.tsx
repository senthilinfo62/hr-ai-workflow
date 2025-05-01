import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import CandidateUpload from './CandidateUpload';
import axios from 'axios';

// Mock axios
vi.mock('axios');

describe('CandidateUpload', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the form correctly', () => {
    render(<CandidateUpload />);
    
    // Check if form elements are rendered
    expect(screen.getByLabelText(/Full Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/CV \(PDF only\)/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Submit/i })).toBeInTheDocument();
  });

  it('shows validation errors for empty fields', async () => {
    render(<CandidateUpload />);
    
    // Submit the form without filling any fields
    fireEvent.click(screen.getByRole('button', { name: /Submit/i }));
    
    // Check if error message is displayed
    expect(await screen.findByText(/Please fill all fields/i)).toBeInTheDocument();
  });

  it('submits the form successfully', async () => {
    // Mock successful axios post
    (axios.post as any).mockResolvedValue({
      data: {
        name: 'John Doe',
        email: 'john@example.com',
        skills: ['JavaScript', 'React'],
        score: 8
      }
    });
    
    render(<CandidateUpload />);
    
    // Fill the form
    fireEvent.change(screen.getByLabelText(/Full Name/i), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'john@example.com' } });
    
    // Mock file input
    const file = new File(['dummy content'], 'resume.pdf', { type: 'application/pdf' });
    const fileInput = screen.getByLabelText(/CV \(PDF only\)/i);
    Object.defineProperty(fileInput, 'files', { value: [file] });
    fireEvent.change(fileInput);
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /Submit/i }));
    
    // Check if axios.post was called with the right arguments
    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledTimes(1);
      expect(axios.post).toHaveBeenCalledWith(
        expect.any(String),
        expect.any(FormData),
        expect.any(Object)
      );
    });
    
    // Check if success message is displayed
    await waitFor(() => {
      expect(screen.getByText(/John Doe/i)).toBeInTheDocument();
      expect(screen.getByText(/john@example.com/i)).toBeInTheDocument();
    });
  });

  it('handles API errors', async () => {
    // Mock failed axios post
    (axios.post as any).mockRejectedValue(new Error('API Error'));
    
    render(<CandidateUpload />);
    
    // Fill the form
    fireEvent.change(screen.getByLabelText(/Full Name/i), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'john@example.com' } });
    
    // Mock file input
    const file = new File(['dummy content'], 'resume.pdf', { type: 'application/pdf' });
    const fileInput = screen.getByLabelText(/CV \(PDF only\)/i);
    Object.defineProperty(fileInput, 'files', { value: [file] });
    fireEvent.change(fileInput);
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /Submit/i }));
    
    // Check if error message is displayed
    await waitFor(() => {
      expect(screen.getByText(/Error submitting CV/i)).toBeInTheDocument();
    });
  });
});
