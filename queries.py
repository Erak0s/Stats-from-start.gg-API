# Une requête qui doit renvoyer les id des tournois qu'on veut analyser
get_all_events_slug="""
query get_all_events_slug($slug: String!, $gameId: [ID]) {
  tournament(slug: $slug) {
    name
    events (filter: {videogameId: $gameId}) {
      name
      id
      }
    }
  }
"""

get_all_events_location="""
query get_events_loc($name: String, $distance: String, $city: String, $perPage: Int, $page: Int, $gameId: [ID], $before: Timestamp, $after: Timestamp) {
  tournaments(
    query: {perPage: $perPage, page: $page, filter: {name: $name, beforeDate: $before, afterDate: $after, location: {distanceFrom: $city, distance: $distance}}}
  ) {
    nodes {
      name
      slug
      city
      countryCode
      postalCode
      startAt
      events (filter: {videogameId: $gameId}) {
        name
        id
        slug
      }
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

# Requête donnant les standings et les seedings de toutes les phases de l'évènement dont on passe l'id.
get_event_standings="""
query get_standings($eventId: ID!, $perPage: Int) {
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
  }
}
"""

get_event_nb_entrants="""
query get_standings($eventId: ID!) {
  event(id: $eventId) {
    id
    name
    numEntrants
  }
}
"""

get_event_seeding="""
query get_seeding($eventId: ID!, $perPage: Int) {
  event(id: $eventId) {
    id
    name
    
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
    sets(perPage: $perPage, sortType: STANDARD) {
      pageInfo {
        totalPages
      }
    }
  }
}
"""

# Returns all sets in the event, with all matches and characters data
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

get_sets_dq="""
query get_sets($eventId: ID!, $page: Int!, $perPage: Int!) {
  event(id: $eventId) {
    id
    name
    sets(
      page: $page
      perPage: $perPage
      sortType: STANDARD
    ) {
      nodes {
        winnerId
        displayScore
        slots {
          entrant {
            name
            id
          }
        }
      }
    }
  }
}
"""

get_sets_no_char="""
query get_sets_no_char($eventId: ID!, $page: Int!, $perPage: Int!) {
  event(id: $eventId) {
    id
    name
    sets(
      page: $page
      perPage: $perPage
      sortType: STANDARD
    ) {
      nodes {
        id
        winnerId
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

get_sets_players="""
query get_sets_no_char($eventId: ID!, $page: Int!, $perPage: Int!) {
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

get_characters="""
query get_characters($eventId: ID!, $page: Int!, $perPage: Int!) {
  event(id: $eventId) {
    sets(
      page: $page
      perPage: $perPage
      sortType: STANDARD
    ) {
      nodes {
        games {
          winnerId
          selections{
            entrant{
              name
              id
            }
            character{
              name
            }
          }
        }
      }
    }
  }
}
"""

get_sets_nogames="""
query get_sets($eventId: ID!, $page: Int!, $perPage: Int!) {
  event(id: $eventId) {
    id
    name
    sets(
      page: $page
      perPage: $perPage
      sortType: STANDARD
    ) {
      nodes {
        winnerId
        displayScore
        slots {
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

# Shorter request to only get the number of sets
get_sets_nb="""
query get_sets_nb($eventId: ID!, $page: Int!, $perPage: Int!) {
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
    }
  }
}
"""

get_all_tournament_data="""
query get_all_tournament_data($eventId: ID!, $page: Int!, $perPage: Int!) {
  event(id: $eventId) {
    id
    name
    phases {
      id
      seeds(query: {perPage: 500}, eventId: $eventId) {
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
    standings(query: {perPage: 500}) {
      nodes {
        placement
        entrant {
          id
          name
        }
      }
    }
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
        displayScore
        slots {
          id
          entrant {
            id
            name
          }
        }
        games {
          winnerId
          selections{
            entrant{
              name
              id
            }
            character{
              name
            }
          }
        }
      }
    }
  }
}
"""