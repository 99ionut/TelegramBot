-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 27, 2020 at 04:56 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `telegrambot`
--

-- --------------------------------------------------------

--
-- Table structure for table `adcampaign`
--

CREATE TABLE `adcampaign` (
  `campaignId` int(11) NOT NULL,
  `title` varchar(128) NOT NULL,
  `description` text NOT NULL,
  `nsfw` tinyint(1) NOT NULL,
  `clicks` int(11) NOT NULL,
  `cpc` float NOT NULL,
  `dailyBudget` float NOT NULL,
  `status` tinyint(1) NOT NULL,
  `url` varchar(512) NOT NULL,
  `username` varchar(128) NOT NULL,
  `country` varchar(100) DEFAULT NULL,
  `totalclicks` int(11) NOT NULL,
  `seconds` int(11) NOT NULL,
  `dateAdded` date DEFAULT NULL,
  `speed` varchar(20) NOT NULL,
  `reports` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `adcampaign`
--

INSERT INTO `adcampaign` (`campaignId`, `title`, `description`, `nsfw`, `clicks`, `cpc`, `dailyBudget`, `status`, `url`, `username`, `country`, `totalclicks`, `seconds`, `dateAdded`, `speed`, `reports`) VALUES
(92, 'ssssssssss', 'fffffffffffffff', 1, 0, 0.0294, 2941, 0, 'http://youtube.com', 'IonutZuZu', 'gb,fr,', 0, 10, '2020-12-06', 'slowest', 0),
(93, 'ssssssssssssss', 'rrrrrrrrrrrrrrrrrrrrr', 0, 0, 0.441, 2941, 0, 'http://twitch.tv', 'IonutZuZu', 'xx', 0, 10, '2020-12-06', 'faster', 3),
(94, 'oooooooooooo', 'ppppppppppppppppp', 0, 0, 0.441, 1471, 0, 'http://wwwwwwwwwww.com', 'IonutZuZu', 'xx', 0, 10, '2020-12-06', 'faster', 0),
(95, 'ooooooooooooo', 'ppppppppppppppp', 0, 0, 0.1471, 2942, 0, 'http://xxxxxxxxxxx.com', 'IonutZuZu', 'gb,fr,', 0, 58, '2020-12-06', 'faster', 0),
(96, 'sssssssss', 'uuuuuuuuuuuuuuuu', 1, 0, 0.4413, 2942, 0, 'http://reddit.com', 'IonutZuZu', 'us,', 0, 10, '2020-12-06', 'fastest', 0),
(97, 'wwwwwwwwwwwwww', 'eeeeeeeeeeeeeeee', 1, 0, 0.0293, 1465, 0, 'http://omega.com', 'IonutZuZu', 'xx', 0, 10, '2020-12-06', 'slowest', 1),
(98, 'wwwwwwwwwwwww', 'kkkkkkkkkkkkkkkkkkk', 0, 0, 0.4405, 2936, 0, 'http://yyyyyyyy.com', 'IonutZuZu', 'xx', 0, 23, '2020-12-06', 'fastest', 0),
(99, 'wwwwwww', 'ggggggggggggg', 0, 0, 0.0293, 73, 1, 'http://youtube.com', 'IonutZuZu', 'xx', 0, 10, '2020-12-06', 'slowest', 0),
(100, 'wwwwwwwwww', 'eeeeeeeeeeeee', 0, 0, 0.1468, 587, 1, 'http://uuuuuuuuuuuu.com', 'IonutZuZu', 'xx', 0, 15, '2020-12-06', 'faster', 0),
(101, 'wwwwwwwwww', 'eeeeeeeeeeeee', 0, 0, 0.4405, 1468, 0, 'http://pppppppp.com', 'IonutZuZu', 'xx', 0, 25, '2020-12-06', 'fastest', 0),
(108, 'rrrrrrrrrr', 'rrrrrrrrrr', 0, 4, 43, 444, 1, 'rrrrrrrrrr.com', 'wwwwwww', 'de', 1, 22, '2020-12-03', 'slow', 0),
(109, 'SESSO GRATISSSS', 'Nane in calore', 1, 0, 0.0221, 1106, 1, 'https://www.pornhub.com', 'cikamoto', 'xx', 0, 10, '2020-12-26', 'slowest', 0),
(110, '😳😳😳😳😳😳😳', '🤡🤡🤡🤡 il tuo bot non funziona 🤡🤡🤡🤡🤡', 1, 0, 0.3318, 1106, 1, 'https://www.pornhub.com/video/search?search=dio+è-ladro', 'cikamoto', 'xx', 0, 10, '2020-12-26', 'fastest', 0);

-- --------------------------------------------------------

--
-- Table structure for table `link`
--

CREATE TABLE `link` (
  `customLink` varchar(64) NOT NULL,
  `username` varchar(128) NOT NULL,
  `campaignId` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `link`
--

INSERT INTO `link` (`customLink`, `username`, `campaignId`) VALUES
('116261211575', 'IonutZuZu', '97');

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `id` int(11) NOT NULL,
  `transaction` varchar(100) NOT NULL,
  `amount` float NOT NULL,
  `userAddress` varchar(100) NOT NULL,
  `userUsername` varchar(100) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `userId` varchar(64) NOT NULL,
  `referral` varchar(64) NOT NULL,
  `taskAlert` tinyint(1) NOT NULL,
  `seeNsfw` tinyint(1) NOT NULL,
  `address` varchar(64) NOT NULL,
  `referredBy` varchar(64) NOT NULL,
  `country` varchar(5) DEFAULT NULL,
  `username` varchar(128) NOT NULL,
  `dateJoined` date DEFAULT NULL,
  `virtualBalance` float NOT NULL DEFAULT 0,
  `lastAd` int(11) NOT NULL DEFAULT -1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userId`, `referral`, `taskAlert`, `seeNsfw`, `address`, `referredBy`, `country`, `username`, `dateJoined`, `virtualBalance`, `lastAd`) VALUES
('286847584', 'fqpEXDli', 1, 1, '2MwjSr1r1gsUTNN5pJGTNkTZDh9FSrkJK5A', '', 'it', 'cikamoto', '2020-12-26', 69, -1),
('626602519', 'bPEKnEKO', 1, 1, '2N6rB1zVJHF3F9hWfwKN9PR24Jm5apah9LT', '', 'en', 'IonutZuZu', NULL, 156, 97),
('oppolo', '', 1, 1, '2N22GhmvbrhfCJv9exKHJ7Gvb5L8qu2H2vE', '', 'uk', 'oppolo', '2020-12-09', 2, -1),
('test', 'wwww', 1, 1, '2N3YcfGc3ozvgUUkZgMQmpjzBVuofChhiLi', '', 'de', 'test', '2020-12-01', 33, -1),
('374408239', 'LdWxuVuw', 1, 1, '2My1b62H5U4uQiYZvd8nXDt1rxdcQUnzGre', '', 'de', 'Trafficbossadmin', NULL, 4, -1),
('666666', 'eeeeee', 1, 1, 'wwwwwwwww', 'wwwwwwwww', 'ww', 'wwwwwww', NULL, 5, -1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `adcampaign`
--
ALTER TABLE `adcampaign`
  ADD PRIMARY KEY (`campaignId`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `link`
--
ALTER TABLE `link`
  ADD PRIMARY KEY (`customLink`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`username`) USING BTREE,
  ADD UNIQUE KEY `address` (`address`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `adcampaign`
--
ALTER TABLE `adcampaign`
  MODIFY `campaignId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=111;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `adcampaign`
--
ALTER TABLE `adcampaign`
  ADD CONSTRAINT `adcampaign_ibfk_2` FOREIGN KEY (`username`) REFERENCES `user` (`username`),
  ADD CONSTRAINT `adcampaign_ibfk_3` FOREIGN KEY (`username`) REFERENCES `user` (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
