//---------------------------------------------------------------------------
//
//	SCSI Target Emulator RaSCSI (*^..^*)
//	for Raspberry Pi
//
//	Copyright (C) 2001-2006 ＰＩ．(ytanaka@ipc-tokai.or.jp)
//	Copyright (C) 2014-2020 GIMONS
//  	Copyright (C) akuker
//
//  	Licensed under the BSD 3-Clause License. 
//  	See LICENSE file in the project root folder.
//
//  	[ SASI device controller ]
//
//---------------------------------------------------------------------------
#pragma once

#include "../config.h"
#include "os.h"
#include "scsi.h"
#include "fileio.h"

class PrimaryDevice;

//===========================================================================
//
//	SASI Controller
//
//===========================================================================
class SASIDEV
{
protected:

private:
	enum sasi_command : int {
		eCmdTestUnitReady = 0x00,
		eCmdRezero =  0x01,
		eCmdRequestSense = 0x03,
		eCmdFormat = 0x04,
		eCmdReadCapacity = 0x05,
		eCmdFormatLegacy = 0x06,
		eCmdReassign = 0x07,
		eCmdRead6 = 0x08,
		eCmdWrite6 = 0x0A,
		eCmdSeek6 = 0x0B,
		eCmdSetMcastAddr  = 0x0D,    // DaynaPort specific command
		eCmdInquiry = 0x12,
		eCmdModeSelect6 = 0x15,
		eCmdReserve6 = 0x16,
		eCmdRelease6 = 0x17,
		eCmdRead10 = 0x28,
		eCmdWrite10 = 0x2A,
		eCmdVerify10 = 0x2E,
		eCmdVerify = 0x2F,
		eCmdModeSelect10 = 0x55,
		eCmdRead16 = 0x88,
		eCmdWrite16 = 0x8A,
		eCmdVerify16 = 0x8F,
		eCmdWriteLong10 = 0x3F,
		eCmdWriteLong16 = 0x9F,
		eCmdInvalid = 0xC2,
		eCmdSasiCmdAssign = 0x0E
	};

public:
	enum {
		UnitMax = 32					// Maximum number of logical units
	};

	const int UNKNOWN_SCSI_ID = -1;
	const int DEFAULT_BUFFER_SIZE = 0x1000;
	// TODO Remove this duplicate
	const int DAYNAPORT_BUFFER_SIZE = 0x1000000;

	// For timing adjustments
	enum {			
		min_exec_time_sasi	= 100,			// SASI BOOT/FORMAT 30:NG 35:OK
		min_exec_time_scsi	= 50
	};

	// Internal data definition
	typedef struct {
		// General
		BUS::phase_t phase;				// Transition phase
		int m_scsi_id;					// Controller ID (0-7)
		BUS *bus;						// Bus

		// commands
		DWORD cmd[16];					// Command data
		DWORD status;					// Status data
		DWORD message;					// Message data

		// Run
		DWORD execstart;				// Execution start time

		// Transfer
		BYTE *buffer;					// Transfer data buffer
		int bufsize;					// Transfer data buffer size
		uint32_t blocks;				// Number of transfer block
		DWORD next;						// Next record
		DWORD offset;					// Transfer offset
		DWORD length;					// Transfer remaining length

		// Logical units
		PrimaryDevice *unit[UnitMax];

		// The current device
		PrimaryDevice *device;

		// The LUN from the IDENTIFY message
		int lun;
	} ctrl_t;

public:
	// Basic Functions
	SASIDEV();
	virtual ~SASIDEV();							// Destructor
	virtual void Reset();						// Device Reset

	// External API
	virtual BUS::phase_t Process(int);				// Run

	// Connect
	void Connect(int id, BUS *sbus);				// Controller connection
	PrimaryDevice* GetUnit(int no);							// Get logical unit
	void SetUnit(int no, PrimaryDevice *dev);				// Logical unit setting
	bool HasUnit();						// Has a valid logical unit

	// Other
	BUS::phase_t GetPhase() {return ctrl.phase;}			// Get the phase

	int GetSCSIID() {return ctrl.m_scsi_id;}					// Get the ID
	ctrl_t* GetCtrl() { return &ctrl; }			// Get the internal information address
	virtual bool IsSASI() const { return true; }		// SASI Check
	virtual bool IsSCSI() const { return false; }		// SCSI check

public:
	void DataIn();							// Data in phase
	void Status();							// Status phase
	void MsgIn();							// Message in phase
	void DataOut();						// Data out phase

	virtual int GetEffectiveLun() const;

	virtual void Error(scsi_defs::sense_key sense_key = scsi_defs::sense_key::NO_SENSE,
			scsi_defs::asc = scsi_defs::asc::NO_ADDITIONAL_SENSE_INFORMATION,
			scsi_defs::status = scsi_defs::status::CHECK_CONDITION);	// Common error handling

protected:
	// Phase processing
	virtual void BusFree();					// Bus free phase
	virtual void Selection();					// Selection phase
	virtual void Command();					// Command phase
	virtual void Execute();					// Execution phase

	// Commands
	void CmdAssign();						// ASSIGN command
	void CmdSpecify();						// SPECIFY command

	// Data transfer
	virtual void Send();						// Send data
	virtual void Receive();					// Receive data

	bool XferIn(BYTE* buf);					// Data transfer IN
	virtual bool XferOut(bool cont);					// Data transfer OUT

	// Special operations
	void FlushUnit();						// Flush the logical unit

	ctrl_t ctrl;								// Internal data
};
