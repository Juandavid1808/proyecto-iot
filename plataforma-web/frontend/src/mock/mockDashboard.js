const mockDashboard = {

    temperatura: 24,
    humedad: 60,
    sonido: 35,
    luz: 300,

    sensores: [

        {
            id: 1,
            tipo_sensor: "temperatura",
            valor: 24,
            unidad: "°C",
            timestamp: "2026-05-15 10:00"
        },

        {
            id: 2,
            tipo_sensor: "humedad",
            valor: 60,
            unidad: "%",
            timestamp: "2026-05-15 10:00"
        },

        {
            id: 3,
            tipo_sensor: "sonido",
            valor: 35,
            unidad: "dB",
            timestamp: "2026-05-15 10:00"
        },

        {
            id: 4,
            tipo_sensor: "luz",
            valor: 300,
            unidad: "lux",
            timestamp: "2026-05-15 10:00"
        }

    ]

}

export default mockDashboard;