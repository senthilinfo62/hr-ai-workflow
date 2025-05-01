// frontend/src/features/cv-submission/CVForm.tsx
import { useForm } from 'react-hook-form';
import axios from 'axios';

export default function CVForm() {
  const { register, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = async (data: any) => {
    const formData = new FormData();
    formData.append('name', data.name);
    formData.append('email', data.email);
    formData.append('cv', data.cv[0]);

    try {
      const response = await axios.post('/api/candidates', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      alert('CV submitted successfully!');
    } catch (error) {
      alert('Error submitting CV');
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">Upload Your CV</h2>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Full Name</label>
          <input
            {...register('name', { required: true })}
            className="w-full p-2 border rounded-md"
          />
          {errors.name && <span className="text-red-500 text-sm">This field is required</span>}
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Email</label>
          <input
            type="email"
            {...register('email', { required: true })}
            className="w-full p-2 border rounded-md"
          />
          {errors.email && <span className="text-red-500 text-sm">This field is required</span>}
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">CV (PDF only)</label>
          <input
            type="file"
            accept=".pdf"
            {...register('cv', { required: true })}
            className="w-full p-2 border rounded-md"
          />
          {errors.cv && <span className="text-red-500 text-sm">This field is required</span>}
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
        >
          Submit Application
        </button>
      </form>
    </div>
  );
}