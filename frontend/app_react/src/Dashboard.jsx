// src/pages/Dashboard.jsx
import React, { useEffect, useState } from 'react';
import AlarmGrid from '../components/AlarmGrid';
import AlarmFilters from '../components/AlarmFilters';
import AlarmStats from '../components/AlarmStats';
import { fetchAlarms } from '../api/api';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import Button from '../components/Button';
import Card from '../components/Card';

const Dashboard = () => {
    const [alarms, setAlarms] = useState([]);
    const [filteredAlarms, setFilteredAlarms] = useState([]);

    useEffect(() => {
        fetchAlarms()
            .then((data) => {
                setAlarms(data);
                setFilteredAlarms(data);  // Initialize filtered alarms with fetched data
            })
            .catch((err) => console.error(err));
    }, []);

    const handleFilterChange = (level) => {
        if (level === 'All') {
            setFilteredAlarms(alarms);
        } else {
            setFilteredAlarms(alarms.filter(alarm => alarm.level === level));
        }
    };

    return (
        <div className="flex">
            <Sidebar />
            <div className="flex-1 p-5">
                <Header />
                <AlarmStats alarms={alarms} />
                <AlarmFilters onFilterChange={handleFilterChange} />
                <Card>
                    <AlarmGrid alarms={filteredAlarms} />
                </Card>
                <Button onClick={() => console.log('Button clicked!')}>Test Button</Button>
            </div>
        </div>
    );
};

export default Dashboard;