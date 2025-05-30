use std::collections::HashMap;

use line_history_rs::traits::SearchByKeywordResult;
use ::line_history_rs::{
    history::OwnedChat,
    traits::{HistoryData, SearchByDate, SearchByKeyword, SearchByRandom},
};
use chrono::{NaiveDate, NaiveTime};
use pyo3::prelude::*;
use pyo3_stub_gen::{define_stub_info_gatherer, derive::{gen_stub_pyclass, gen_stub_pymethods}};

#[gen_stub_pyclass]
#[pyclass(frozen)]
pub struct History {
    history: ::line_history_rs::history::OwnedHistory,
}

#[gen_stub_pymethods]
#[pymethods]
impl History {
    #[new]
    fn new(days: HashMap<NaiveDate, Py<Day>>) -> Self {
        let days = days
            .iter()
            .map(|(&date, day)| {
                (date, day.get().day.as_ref_day())
            });

        History {
            history: ::line_history_rs::history::History::new(days.collect()).into_owned(),
        }
    }

    #[staticmethod]
    pub fn read_from_file(path: String) -> Self {
        ::line_history_rs::read_from_file!(path,  let src, let history);
        let history = ::line_history_rs::history::ignore_errors(history);

        Self { history: history.into() }
    }

    #[staticmethod]
    pub fn from_text(text: String) -> Self {
        Self {
            history: ::line_history_rs::history::History::from_text(&text).into_owned(),
        }
    }

    pub fn search_by_date(&self, date: NaiveDate) -> Option<Day> {
        self.history
            .search_by_date(&date)
            .map(|owned_day| Day::from(owned_day.clone()))
    }

    pub fn search_by_keyword(&self, keyword: &str) -> Vec<(NaiveDate, Chat)> {
        self.history
            .search_by_keyword(keyword)
            .map(|SearchByKeywordResult { date, chat, .. }| (date, Chat::from(chat.clone())))
            .collect()
    }

    pub fn search_by_random(&self) -> Day {
        let day = self.history.search_by_random();
        Day::from(day.clone())
    }

    pub fn days(&self) -> HashMap<NaiveDate, Day> {
        self.history
            .days()
            .iter()
            .map(|(&date, owned_day)| (date, Day::from(owned_day.clone())))
            .collect()
    }

    pub fn len(&self) -> usize {
        self.history.len()
    }

    pub fn is_empty(&self) -> bool {
        self.history.is_empty()
    }
}

#[gen_stub_pyclass]
#[pyclass(frozen)]
pub struct Day {
    day: ::line_history_rs::history::OwnedDay,
}

impl From<Day> for ::line_history_rs::history::OwnedDay {
    fn from(value: Day) -> Self {
        value.day
    }
}

impl From<::line_history_rs::history::OwnedDay> for Day {
    fn from(owned_day: ::line_history_rs::history::OwnedDay) -> Self {
        Day {
            day: owned_day,
        }
    }
}

#[gen_stub_pymethods]
#[pymethods]
impl Day {
    pub fn date(&self) -> NaiveDate {
        self.day.date
    }

    pub fn chats(&self) -> Vec<Chat> {
        self.day.chats
            .iter()
            .map(|owned_chat| Chat::from(owned_chat.clone()))
            .collect()
    }

    pub fn search_by_keyword(&self, keyword: &str) -> Vec<(NaiveDate, Chat)> {
        self.day.search_by_keyword(keyword).map(|SearchByKeywordResult { date, chat, .. }| (date, Chat::from(chat.clone()))).collect()
    }
}

#[gen_stub_pyclass]
#[pyclass(frozen)]
pub struct Chat {
    chat: ::line_history_rs::history::OwnedChat,
}

impl From<OwnedChat> for Chat {
    fn from(owned_chat: OwnedChat) -> Self {
        Chat {
            chat: owned_chat,
        }
    }
}

#[gen_stub_pymethods]
#[pymethods]
impl Chat {
    pub fn time(&self) -> NaiveTime {
        self.chat.time
    }

    pub fn speaker(&self) -> &Option<String> {
        &self.chat.speaker
    }

    pub fn message_lines(&self) -> &Vec<String> {
        &self.chat.message_lines
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn line_history(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<History>()?;
    m.add_class::<Day>()?;
    m.add_class::<Chat>()?;
    Ok(())
}

define_stub_info_gatherer!(stub_info);
