# Une requête qui doit renvoyer les id des tournois qu'on veut analyser
get_all_events_slug="""
query get_all_events_slug($slug: String!, $gameId: [ID]) {
  tournament(slug: $slug) {
    name
    events (filter: {videogameId: $gameId}) {
      name
      id
      isOnline
      numEntrants
      }
    }
  }
"""

get_all_events_location_pages="""
query get_events_loc($name: String, $distance: String, $city: String, $perPage: Int, $page: Int, $gameId: [ID], $before: Timestamp, $after: Timestamp) {
  tournaments(
    query: {perPage: $perPage, page: $page, filter: {name: $name, beforeDate: $before, afterDate: $after, videogameIds: $gameId, location: {distanceFrom: $city, distance: $distance}}}
  ) {
    pageInfo{
    total
      totalPages
    }
  }
}
"""

get_all_events_location="""
query get_events_loc($name: String, $distance: String, $city: String, $perPage: Int, $page: Int, $gameId: [ID], $before: Timestamp, $after: Timestamp) {
  tournaments(
    query: {perPage: $perPage, page: $page, filter: {name: $name, beforeDate: $before, afterDate: $after, videogameIds: $gameId, location: {distanceFrom: $city, distance: $distance}}}
  ) {
    nodes {
      id
      name
      events {
          id
          name
          numEntrants
          isOnline
      }
    }
  }
}
"""

get_all_events_no_location_pages="""
query get_events_no_loc($name: String, $cCode: String, $perPage: Int, $page: Int, $gameId: [ID], $before: Timestamp, $after: Timestamp) {
  tournaments(
    query: {perPage: $perPage, page: $page filter: {name: $name, countryCode: $cCode, beforeDate: $before, afterDate: $after}}
  ) {
    pageInfo{
    total
      totalPages
    }
  }
}
"""

get_all_events_no_location="""
query get_events_no_loc($name: String, $cCode: String, $perPage: Int, $page: Int, $gameId: [ID], $before: Timestamp, $after: Timestamp) {
  tournaments(
    query: {perPage: $perPage, page: $page filter: {name: $name, countryCode: $cCode, beforeDate: $before, afterDate: $after}}
  ) {
    nodes {
      name
      slug
      countryCode
      postalCode
      events (filter: {videogameId: $gameId}) {
        name
        id
      }
    }
  }
}
"""

get_event_seeding_standing="""
query get_seeding($eventId: ID!, $perPage: Int) {
  event(id: $eventId) {
    id
    name
    standings(query: {perPage: $perPage}) {
      nodes {
        placement
        entrant {
          id
          name
        }
      }
    }
    phases {
      id
      seeds(query: {perPage: $perPage}, eventId: $eventId) {
        nodes {
          id
          seedNum
          entrant {
            id
            name
          }
        }
      }
    }
  }
}
"""

get_sets_pages="""
query get_sets($eventId: ID!, $perPage: Int!) {
  event(id: $eventId) {
    sets(
      perPage: $perPage
      sortType: STANDARD
    ) {
      pageInfo {
        totalPages
      }
    }
  }
}
"""

get_sets="""
query get_sets($eventId: ID!, $page: Int!, $perPage: Int!) {
  event(id: $eventId) {
    id
    name
    sets(
      page: $page
      perPage: $perPage
      sortType: STANDARD
    ) {
      pageInfo {
        total
      }
      nodes {
        id
        winnerId
        games {
          winnerId
          selections{
            character{
              name
            }
          }
        }
        slots {
          id
          entrant {
            id
            name
          }
        }
      }
    }
  }
}
"""
