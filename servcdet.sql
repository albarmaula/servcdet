-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 17, 2024 at 09:17 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `servcdet`
--

-- --------------------------------------------------------

--
-- Table structure for table `detection`
--

CREATE TABLE `detection` (
  `detection_id` int(11) NOT NULL,
  `image` longtext NOT NULL,
  `label` varchar(200) NOT NULL,
  `time` timestamp NOT NULL DEFAULT current_timestamp(),
  `patient_id` int(11) NOT NULL,
  `note` varchar(5000) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `confidence` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `detection`
--

INSERT INTO `detection` (`detection_id`, `image`, `label`, `time`, `patient_id`, `note`, `user_id`, `confidence`, `status`) VALUES
(1, 'det_4ac16a54-2150-11ef-879f-b06ebf1f7c31_153955676-153955721-001.BMP', 'normal', '2024-05-14 08:03:19', 1, '-Tidak ada kelainan\n-normal', 2, '80', 'non-aktif'),
(2, 'det_4ac16a54-2150-11ef-879f-b06ebf1f7c31_153955676-153955721-001.BMP', 'abnormal', '2024-06-14 08:03:19', 1, NULL, 2, '80', 'aktif'),
(3, 'det_4ac16a54-2150-11ef-879f-b06ebf1f7c31_153955676-153955721-001.BMP', 'abnormal', '2024-06-14 08:03:19', 1, NULL, 2, '75', 'aktif'),
(4, 'det_4ac16a54-2150-11ef-879f-b06ebf1f7c31_153955676-153955721-001.BMP', 'abnormal', '2024-06-14 08:03:19', 1, NULL, 2, '75', 'aktif'),
(37, 'det_b9ecaf15-2ae6-11ef-b997-409f38674562_157183828-157183877-001.BMP', 'normal', '2024-06-15 07:13:22', 1, '-Tidak ada kelainan\n-normal', 2, '90.06107661833367', 'aktif'),
(38, 'det_b7d6f83a-2af7-11ef-a997-409f38674562_153956279-153956296-001.BMP', 'abnormal', '2024-06-15 09:14:59', 3, 'percobaan', 2, '85.80004436406912', 'aktif'),
(39, 'det_1fe0f970-2af8-11ef-bc3b-409f38674562_153955676-153955721-001.BMP', 'normal', '2024-06-15 09:17:46', 2, '-Tidak ada kelainan -normal', 2, '90.20014168221728', 'aktif'),
(40, 'det_8878a9c3-2af8-11ef-9a21-409f38674562_157222647-157222687-001.BMP', 'normal', '2024-06-15 09:20:41', 4, '-Tidak ada kelainan\n-normal', 2, '92.02862337923716', 'aktif'),
(41, 'det_a0fa54ae-2af8-11ef-b4f9-409f38674562_157222801-157222811-002.BMP', 'normal', '2024-06-15 09:21:22', 3, '-Tidak ada kelainan\n-normal', 2, '92.16625810699365', 'aktif'),
(42, 'det_60e25c75-2afa-11ef-af19-409f38674562_157183332-157183388-002.BMP', 'normal', '2024-06-15 09:33:54', 2, '-Tidak ada kelainan\r\n-normal', 2, '89.41389245548005', 'aktif'),
(43, 'det_b713527d-3fb6-11ef-8a75-409f38674562_153958345-153958392-001.BMP', 'abnormal', '2024-07-11 18:52:40', 1, '', 2, '71.28640387648835', 'aktif'),
(44, 'det_faa4b614-3fb6-11ef-9ec4-409f38674562_157181671-157181686-001.BMP', 'normal', '2024-07-11 18:54:19', 1, '', 2, '88.5512553422646', 'aktif'),
(45, 'det_e835d87b-3fb9-11ef-88fe-409f38674562_NL_1__10.jpg', 'normal', '2024-07-11 19:15:17', 1, '', 2, '92.4607006780852', 'aktif'),
(46, 'det_efb60a38-3fb9-11ef-8071-409f38674562_NL_3__5.jpg', 'normal', '2024-07-11 19:15:29', 1, '', 2, '91.47729926424537', 'aktif'),
(47, 'det_f44d70f1-3fb9-11ef-b5cc-409f38674562_NL_5__3.jpg', 'abnormal', '2024-07-11 19:15:37', 1, '', 2, '66.74431082368352', 'aktif'),
(48, 'det_002b2899-3fba-11ef-82d4-409f38674562_NL_30__6.jpg', 'abnormal', '2024-07-11 19:15:57', 1, '', 2, '86.21110771989954', 'aktif'),
(49, 'det_064be71d-3fba-11ef-b615-409f38674562_scc_1_9.jpg', 'abnormal', '2024-07-11 19:16:07', 1, '', 2, '85.7233450533998', 'aktif'),
(50, 'det_0b255a54-3fba-11ef-9855-409f38674562_scc_2_3.jpg', 'abnormal', '2024-07-11 19:16:15', 1, '', 2, '85.69551848853708', 'aktif'),
(51, 'det_0f39217f-3fba-11ef-904c-409f38674562_SCC_4_1.jpg', 'normal', '2024-07-11 19:16:22', 1, '', 2, '86.23014278286445', 'aktif'),
(52, 'det_918eb73e-3ff2-11ef-b1a1-409f38674562_scc_1_1.jpg', 'abnormal', '2024-07-12 02:01:10', 2, NULL, 2, '86.26988804019278', 'aktif'),
(53, 'det_0157d547-3ff3-11ef-a6f7-409f38674562_153958547-153958572-003.BMP', 'abnormal', '2024-07-12 02:04:01', 1, '', 2, '85.6955718559852', 'aktif'),
(54, 'det_5b4b8d1b-4406-11ef-9545-aa3f0eedc792_153955676-153955721-001.BMP', 'normal', '2024-07-17 06:32:43', 3, '-ga ada kelainan', 2, '90.19706200011684', 'aktif'),
(55, 'det_888edc50-4407-11ef-a5d3-aa3f0eedc792_scc_1_1.jpg', 'abnormal', '2024-07-17 06:41:03', 1, '', 2, '86.26988804019278', 'aktif'),
(56, 'det_aef5bdf1-4408-11ef-8495-aa3f0eedc792_153955676-153955721-001.BMP', 'normal', '2024-07-17 06:49:23', 1, '', 2, '90.19706200011684', 'aktif');

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE `patient` (
  `id` int(50) NOT NULL,
  `nik` varchar(20) NOT NULL,
  `username` varchar(200) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `birthday` date NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `status` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`id`, `nik`, `username`, `phone`, `birthday`, `date`, `status`) VALUES
(1, '35781565980003', 'Anisa', '081234568989', '2011-06-15', '2024-06-12 22:16:20', 'belum menikah'),
(2, '35782312320001', 'Siti', '085657579212', '2024-06-15', '2024-06-15 10:53:12', 'menikah'),
(3, '35781123210002', 'Sari', '081256871456', '2024-06-13', '2024-06-15 10:53:33', 'belum menikah'),
(4, '35786512010002', 'Sumini', '085654872369', '2024-05-28', '2024-06-15 10:54:01', 'belum menikah');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(1000) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `role` varchar(10) NOT NULL,
  `status` varchar(10) NOT NULL,
  `profile_picture` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `username`, `phone`, `email`, `password`, `created_at`, `role`, `status`, `profile_picture`) VALUES
(1, 'Widaad Albar Maula', '085649415981', 'albarmaula@gmail.com', 'scrypt:32768:8:1$dClYVByZuKI2rQd4$00589dfb5c862d2afae4fe4ecf2426c1972ac466341753fbc1f12e8f7fc8c08676880b52b012221ec63943cc556ad242eb98cd06d2e3d88498b93e7842762517', '2024-03-24 17:00:00', 'superadmin', 'aktif', 'pp_410dfb5a-fe56-11ee-8925-b06ebf1f7c31_farhan.png'),
(2, 'Adudu Adidi', '085658541256', 'bukanalbarmaula@gmail.com', 'scrypt:32768:8:1$FeE1JzaRzAkqqyUH$dcdb9eac7c8ff5da16335101cab86600ee5464165fc1c7e62e2d0656c15242c54d57b878b92c26dafec9c6116111109e71c8403a5d6fcb40abcba414f141d062', '2024-03-29 17:00:00', 'dokter', 'aktif', 'pp_d1e67170-f7f6-11ee-8081-b06ebf1f7c31_Foto.png'),
(6, 'Lala Lele', '081259709492', 'asd@gmail.com', 'scrypt:32768:8:1$0oP4aARporv6cgiF$d3840c839d4cfb087f2bde79d22710c373372416077ddf75c34a264fa18ca4077ce7bbe27a5e25c6bbcffe9b802bb740108b59add6935f8a23ab0a55299a2cd0', '2024-05-01 12:53:04', 'dokter', 'non-aktif', 'user-black.png'),
(7, 'Mina Mino', '085649872121', 'admin@gmail.com', 'scrypt:32768:8:1$ZUo2fAGHpPezqUbz$6c2135e317b7dfb7383758c2c126ef5ff0671ef4d9c5c2d1b0a6f0ed1cd5af4473bde8531a31cac4dadfdaf5cfd657083c40cc88faeadf4bd6f3d1efc3617df0', '2024-06-12 10:16:16', 'admin', 'aktif', 'user-black.png'),
(9, 'Santi Sinta', '081256849512', 'tes2@gmail.com', 'scrypt:32768:8:1$tfYXk9HoY6syJqG2$a5f5dbc0b268031c5d61298989a38e74b6a7a546528dbae720768dae09336732237a469bbea107446c202314375c3a400cb1549a43f513db3740a7698c8f5828', '2024-06-12 11:15:42', 'admin', 'non-aktif', 'user-black.png'),
(10, 'Delle Ali', '081259709492', 'tes3@gmail.com', 'scrypt:32768:8:1$EpKE28M6ogPQ4LxI$525dae229b21af488bd566acbc0e928c7485fa29be4747bf6d689de651e519e1bb16086a3551bfbaf7e477a9a33aaaf3394e43108b455f3dc0626ecb344489eb', '2024-06-12 11:17:39', 'superadmin', 'aktif', 'user-black.png'),
(11, 'Gareth Southgate', '085648953215', 'dokter@gmail.com', 'scrypt:32768:8:1$RN6zhtuDbdtC0hL7$332462a52e1e35f1262488e8d670d0c458d45092022f4ba6ff2f7d6d8b8e3707811fd6f69538a38456952aad3faeae96f5358fafa011594997a6d2d4ff22d7a5', '2024-06-15 04:16:14', 'dokter', 'aktif', 'user-black.png');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `detection`
--
ALTER TABLE `detection`
  ADD PRIMARY KEY (`detection_id`);

--
-- Indexes for table `patient`
--
ALTER TABLE `patient`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `detection`
--
ALTER TABLE `detection`
  MODIFY `detection_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT for table `patient`
--
ALTER TABLE `patient`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
