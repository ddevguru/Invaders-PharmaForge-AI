import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Signup from './pages/Signup';
import UserDashboard from './pages/dashboard/User';
import AdminDashboard from './pages/dashboard/Admin';
import WarehouseDashboard from './pages/dashboard/Warehouse';
import PharmacistDashboard from './pages/dashboard/Pharmacist';
import VoiceTraining from './pages/VoiceTraining';
import VoiceAgent from './components/VoiceAgent';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route 
          path="/dashboard/user" 
          element={
            <ProtectedRoute allowedRoles={['user', 'admin']}>
              <VoiceAgent />
              <UserDashboard />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/dashboard/admin" 
          element={
            <ProtectedRoute allowedRoles={['admin']}>
              <VoiceAgent />
              <AdminDashboard />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/dashboard/warehouse" 
          element={
            <ProtectedRoute allowedRoles={['warehouse', 'admin']}>
              <VoiceAgent />
              <WarehouseDashboard />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/dashboard/pharmacist" 
          element={
            <ProtectedRoute allowedRoles={['pharmacist', 'admin']}>
              <VoiceAgent />
              <PharmacistDashboard />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/voice-training" 
          element={
            <ProtectedRoute>
              <VoiceTraining />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </Router>
  );
}

export default App;