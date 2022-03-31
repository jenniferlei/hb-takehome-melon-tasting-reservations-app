"use strict";

const startTimes = [
  "00:00",
  "00:30",
  "01:00",
  "01:30",
  "02:00",
  "02:30",
  "03:00",
  "03:30",
  "04:00",
  "04:30",
  "05:00",
  "05:30",
  "06:00",
  "06:30",
  "07:00",
  "07:30",
  "08:00",
  "08:30",
  "09:00",
  "09:30",
  "10:00",
  "10:30",
  "11:00",
  "11:30",
  "12:00",
  "12:30",
  "13:00",
  "13:30",
  "14:00",
  "14:30",
  "15:00",
  "15:30",
  "16:00",
  "16:30",
  "17:00",
  "17:30",
  "18:00",
  "18:30",
  "19:00",
  "19:30",
  "20:00",
  "20:30",
  "21:00",
  "21:30",
  "22:00",
  "22:30",
  "23:00",
  "23:30",
];

const ViewReservation = (props) => {};

const ViewReservationContainer = (props) => {};

const AvailableReservation = (props) => {};

const SearchReservation = (props) => {
  const [reservationDate, setReservationDate] = React.useState("");
  const [reservationStart, setReservationStart] = React.useState("");
  const [reservationEnd, setReservationEnd] = React.useState("");

  const [openReservations, setOpenReservations] = React.useState("");

  React.useEffect(() => {
    // fetch all
    fetch();
  }, []);

  // fetch reservations based on the date, start time and end time parameters
  // if user already has a reservation on date, show error
  // if none available, show error
  const getOpenReservations = () => {
    if (reservationDate === "") {
      alert("Please input a date");
    } else {
      const queries = ["/search_reservations?"];
      queries.push(`date=${reservationDate}`);
      if (reservationStart !== "") {
        queries.push(`start_time=${reservationStart}`);
      }
      if (reservationEnd !== "") {
        queries.push(`end_time=${reservationEnd}`);
      }
      const queriesUrl = queries.reduce(
        (text, value, i, array) => text + (i > 1 ? "&" : "") + value
      );

      fetch(queriesUrl)
        .then((response) => response.json())
        .then((responseJson) => {
          const { reservations } = responseJson;

          setOpenReservations(availReservations);
        });
    }
  };

  return (
    <div>
      <h3>Make A Reservation</h3>
      Enter the Date of the reservation you would like
      <div className="mb-1">
        <label htmlFor="reservationDate"> Date </label>
        <input
          type="date"
          value={reservationDate}
          onChange={(event) => setReservationDate(event.target.value)}
          className="form-control"
          id="reservationDate"
        />
      </div>
      Enter an optional time range and we will only show appointments in that
      range
      <div className="row">
        <div className="col mb-1">
          <label htmlFor="reservationStart"> Start Time </label>
          <input
            type="time"
            value={reservationStart}
            onChange={(event) => setReservationStart(event.target.value)}
            className="form-control"
            id="reservationStart"
          />
        </div>
        <div className="col mb-1">
          <label htmlFor="reservationEnd"> End Time </label>
          <input
            type="time"
            value={reservationEnd}
            onChange={(event) => setReservationEnd(event.target.value)}
            className="form-control"
            id="reservationEnd"
          />
        </div>
      </div>
      <button
        type="submit"
        className="btn btn-outline-dark"
        data-bs-dismiss="modal"
        onClick={getOpenReservations}
      >
        Search
      </button>
    </div>
  );
};

const ReservationContainer = (props) => {
  return (
    <div
      className="card"
      style={{
        top: "1.5em",
        width: "90vw",
        height: "80vh",
        margin: "auto",
        backgroundColor: "rgba(255, 255, 255, 0.9)",
      }}
    >
      <div className="card-body">
        <div className="col-6">
          <SearchReservation />
        </div>
        <div className="col-6">
          <ViewReservationContainer />
        </div>
      </div>
    </div>
  );
};

ReactDOM.render(<ReservationContainer />, document.getElementById("root"));
